import os
import time

from libpipe import futils

from . import skymodel, cal, flagutils


def get_all_tasks():
    d = {}
    for klass in AbstractTask.__subclasses__():
        if hasattr(klass, 'name'):
            d[klass.name] = klass
    return d


def get_all_tasks_descriptions():
    d = {}
    for klass in AbstractTask.__subclasses__():
        if hasattr(klass, 'name') and hasattr(klass, 'desc'):
            d[klass.name] = klass.desc
    return d


class AbstractTask(object):

    def __init__(self, s_task, s_worker, s_skymodel):
        self.s_task = s_task
        self.s_worker = s_worker
        self.s_skymodel = s_skymodel

    def run(self, msins):
        pass


class BuildSkyModel(AbstractTask):

    name = 'build_sky_model'
    desc = 'Build sky model'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        if self.s_skymodel.int_sky_model in skymodel.sky_model_catalogs:
            int_sky_model = f'catalog_intrinsic_{self.s_skymodel.int_sky_model}.skymodel'
            if not self.s_worker.dry_run:
                skymodel.build_sky_model_ms(msins[0], self.s_task.min_flux, self.s_task.catalog_radius, int_sky_model,
                                            catalog=self.s_skymodel.int_sky_model)
        elif os.path.exists(self.s_skymodel.int_sky_model):
            int_sky_model = self.s_skymodel.int_sky_model
        else:
            print('Intrinsic sky model not found. Can be either a file or one of the catalog: lcs165 or specfinf.')
            return []

        cal.MakeAppSkyModel(self.s_worker, self.s_skymodel.app_sky_model_name, int_sky_model, self.s_task).run(msins)
        cal.MakeSourceDB(self.s_worker, self.s_skymodel.app_sky_model_name, self.s_task).run(msins)

        return msins


class RestoreFlags(AbstractTask):

    name = 'restore_flags'
    desc = 'Restore or Backup flags'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        cal.RestoreOrBackupFlag(self.s_worker, self.s_task.flag_name).run(msins)

        return msins


class DDECal(AbstractTask):

    name = 'ddecal'
    desc = 'Direction dependent calibration'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        cal_settings = cal.CalSettings(**self.s_task.cal)
        sky_model = cal.SkyModel(self.s_skymodel.app_sky_model_name)

        if self.s_task.avg.time == 1 and self.s_task.avg.freq == 1:
            cal.DDEcal(self.s_worker, cal_settings, sky_model, data_col=self.s_task.col_in,
                       directions=self.s_task.directions).run(msins)
        else:
            mstemps = cal.DDEcalAvg(self.s_worker, cal_settings, sky_model, data_col=self.s_task.col_in,
                                    directions=self.s_task.directions, time_avg=self.s_task.avg.time,
                                    freq_avg=self.s_task.avg.freq).run(msins)
            futils.zip_rm(mstemps)

        if self.s_task.do_smooth_sol:
            futils.zip_copy(msins, msins, cal_settings.parmdb, filename_out=cal_settings.parmdb + '.bck')
            cal.SmoothSolutions(self.s_worker, cal_settings.parmdb, **self.s_task.smooth_sol).run(msins)

        if self.s_task.plot_sol:
            cal.PlotSolutions(self.s_worker, cal_settings.parmdb).run(msins)

        return msins


class Flagger(AbstractTask):

    name = 'flagger'
    desc = 'Pre/post calibration flagging'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        if self.s_task.do_aoflagger:
            cal.FlagPostCal(self.s_worker, self.s_task.aoflagger.strategy).run(msins)

        if self.s_task.do_baselinesflag:
            cal.FlagBaselines(self.s_worker, self.s_task.baselinesflag.baselines).run(msins)

        if self.s_task.do_flagfreq:
            cal.FlagFreqs(self.s_worker, self.s_task.flagfreq.fmhz_range).run(msins)

        if self.s_task.do_badbaselines:
            cal.AoQuality(self.s_worker).run(msins)
            cal.FlagBadBaselines(self.s_worker, **self.s_task.badbaselines).run(msins)

        if self.s_task.do_ssins:
            cal.SSINSFlagger(self.s_worker, config=self.s_task.ssins.seetings, plot_dir='flag_plot').run(msins)

        if self.s_task.do_scans_flagging:
            print('Start scans flagging ...')
            flagutils.flag_badscans(msins, data_col='CORRECTED_DATA', nsigma=self.s_task.scans_flagging.nsigma_scans)

        cal.AoQuality(self.s_worker).run(msins)

        return msins


class SmoothSolutions(AbstractTask):

    name = 'multims_smooth_sol'
    desc = 'Smooth Solutions over multiple MS'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        from .smoothsol import smooth_solutions

        smooth_solutions(msins, self.s_task.parmdb_in, self.s_task.parmdb_out, plot_dir=self.s_task.plot_dir)

        return msins


class ApplyCal(AbstractTask):

    name = 'apply_cal'
    desc = 'Apply calibration'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        cal_settings = cal.CalSettings(**self.s_task.cal)

        cal.ApplyCal(self.s_worker, cal_settings, self.s_task.col_in, self.s_task.col_out,
                     direction=self.s_task.direction).run(msins)

        return msins


class Subtract(AbstractTask):

    name = 'subtract'
    desc = 'Subtract sources'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        cal_settings = cal.CalSettings(**self.s_task.cal)
        sky_model = cal.SkyModel(self.s_skymodel.app_sky_model_name)
        cal.Subtract(self.s_worker, cal_settings, sky_model, self.s_task.col_in,
                     self.s_task.col_out, directions=self.s_task.directions).run(msins)

        return msins


class PeelCal(AbstractTask):

    name = 'peel'
    desc = 'Peel calibration'

    def __init__(self, s_task, s_worker, s_skymodel):
        AbstractTask.__init__(self, s_task, s_worker, s_skymodel)

    def run(self, msins):
        cal_settings_init = cal.CalSettings(**self.s_task.init)
        sky_model = cal.SkyModel(self.s_skymodel.app_sky_model_name)

        # Start with a new MS
        msouts = cal.CopyMS(self.s_worker, 'DATA', self.s_task.ms_postfix).run(msins)

        # Copy initial calibration table from .MS to _PEEL.MS
        futils.zip_copy(msins, msouts, cal_settings_init.parmdb)
        sky_model.copy(msins, msouts)

        for i, mspeel in cal.Peel(sky_model).iterations(msouts):
            cal_settings_iter = cal.CalSettings(**self.s_task.cal)
            cal_settings_iter.parmdb = f'instrument_peel_iter{i}.h5'

            if self.s_task.do_phase_shift:
                mstemps = cal.PeelPreSubtractPhaseShifted(i, self.s_worker, cal_settings_init, sky_model,
                                                          **self.s_task.phase_shift).run(mspeel)

                sky_model.copy(mspeel, mstemps)
                cal.PeelCal(i, self.s_worker, cal_settings_iter, sky_model, data_col='DATA').run(mstemps)

                if self.s_task.do_smooth_sol:
                    cal.SmoothSolutions(self.s_worker, cal_settings_iter.parmdb, **self.s_task.smooth_sol).run(mstemps)

                futils.zip_copy(mstemps, mspeel, cal_settings_iter.parmdb)
                futils.zip_rm(mstemps)

                mstemps = cal.PeelPostSubtractPhaseShift(i, self.s_worker, cal_settings_iter, sky_model).run(mspeel)

                time.sleep(1)

                futils.zip_rename_reg(mspeel, mstemps, 'table|^[A-Z]', invert=True)
                futils.zip_rm(mspeel)
                futils.zip_rename(mstemps, mspeel)
            else:
                cal.PeelPreSubtract(i, self.s_worker, cal_settings_init, sky_model).run(mspeel)
                cal.PeelCal(i, self.s_worker, cal_settings_iter, sky_model).run(mspeel)
                cal.PeelPostSubtract(i, self.s_worker, cal_settings_iter, sky_model).run(mspeel)

            cal.PlotSolutions(self.s_worker, cal_settings_iter.parmdb).run(mspeel)

        return msouts
