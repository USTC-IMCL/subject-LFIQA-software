import ScoringWidget
import sys
sys.path.append("../Utils")

import ExpInfo
from ScoringWidget import PairWiseScoringWidget, ScoringWidget
from ExpInfo import ComparisonType
from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtWidgets import QApplication
import logging
import time
logger=logging.getLogger("LogWindow")

class ExperimentSession(QObject):
    '''
    A single evaluation session bound to one ComparisonType.
    Optionally splits the trial list into smaller chunks so a break
    dialog can be shown every N trials or every M minutes (fatigue
    management, not algorithm phases).
    '''
    exp_finished = Signal()
    session_should_break = Signal(int, int)   # (done, total)

    def __init__(self, show_list: ExpInfo.AllScoringLFI,
                 exp_setting: ExpInfo.ExpSetting = None,
                 mode="training",
                 comparison_type: ComparisonType = ComparisonType.DoubleStimuli,
                 trials_per_session: int = 0,
                 minutes_per_session: int = 0):
        super().__init__()
        self.exp_setting = exp_setting
        self.exp_mode = mode
        self.all_scoring_lfi = show_list

        # Session identity — fixed at construction time
        self.comparison_type = comparison_type
        self.trials_per_session = trials_per_session
        self.minutes_per_session = minutes_per_session

        self.subject_info = None
        self.scoring_page = None
        self.screen_index = 0

        # Results
        self.result = []
        self.show_index = []

        # Internal batch tracking
        self._remaining_index = []
        self._session_start_time = 0.0
        self._time_timer = None
        self._need_break = False

    def SetSubjectInfo(self, subject_info: ExpInfo.PersonInfo):
        self.subject_info = subject_info

    def SetScreenIndex(self, screen_index: int):
        self.screen_index = screen_index

    def Start(self):
        self.result = []
        self._need_break = False

        show_lfi_num = self.all_scoring_lfi.GetLFINum()
        if show_lfi_num == 0:
            self.exp_finished.emit()
            return

        if self.exp_mode.lower() == "training":
            all_show_index = list(range(show_lfi_num))
        else:
            all_show_index = self.all_scoring_lfi.GetRandomShowOrder()
        self.show_index = all_show_index

        self._remaining_index = list(all_show_index)
        self._session_start_time = time.time()

        if self.minutes_per_session > 0 and self._time_timer is None:
            self._time_timer = QTimer()
            self._time_timer.timeout.connect(self._check_time)
            self._time_timer.start(10000)

        self._run_batch()

    def _run_batch(self):
        if not self._remaining_index:
            self._finish()
            return

        batch_size = self.trials_per_session if self.trials_per_session > 0 else len(self._remaining_index)
        batch_index = self._remaining_index[:batch_size]
        self._remaining_index = self._remaining_index[batch_size:]

        logger.debug("=========Playing List (Batch)=========")
        for i in batch_index:
            tmp = self.all_scoring_lfi.GetScoringExpLFIInfo(i)
            logger.debug(f"Index: {i}, Path: {tmp.passive_view_video_path}")
        logger.debug("=========    End    =========")

        if self.comparison_type == ComparisonType.PairComparison:
            self.scoring_page = PairWiseScoringWidget(self.all_scoring_lfi, self.exp_setting, batch_index)
        else:
            self.scoring_page = ScoringWidget(self.all_scoring_lfi, self.exp_setting, batch_index)

        self.scoring_page.trial_scored.connect(self._on_trial_scored)
        self.scoring_page.scoring_finished.connect(self._on_batch_finished)

        app = QApplication.instance()
        if app is None:
            app = QApplication([])
        self.scoring_page.setScreen(app.screens()[self.screen_index])
        cur_screen = self.scoring_page.screen()
        self.scoring_page.move(cur_screen.geometry().topLeft())
        self.scoring_page.SetScoringScreen(self.screen_index)
        self.scoring_page.showFullScreen()

    def _on_trial_scored(self, done, total):
        pass

    def _check_time(self):
        if self.minutes_per_session <= 0:
            return
        elapsed = time.time() - self._session_start_time
        if elapsed >= self.minutes_per_session * 60:
            self._need_break = True

    def _on_batch_finished(self, batch_scores):
        if self.scoring_page is not None:
            self.scoring_page.trial_scored.disconnect(self._on_trial_scored)
            self.scoring_page.scoring_finished.disconnect(self._on_batch_finished)
            self.scoring_page.hide()
            self.scoring_page.deleteLater()
            self.scoring_page = None

        if isinstance(batch_scores, list) and len(batch_scores) > 0:
            if isinstance(batch_scores[0], list):
                for s in batch_scores:
                    self.result.append(s)
            else:
                self.result.append(batch_scores)

        elapsed = time.time() - self._session_start_time
        need_time_break = self._need_break or (
            self.minutes_per_session > 0 and
            elapsed >= self.minutes_per_session * 60)

        if self._remaining_index and (need_time_break or self.trials_per_session > 0):
            done_trials = len(self.result) if isinstance(self.result, list) else 1
            self.session_should_break.emit(done_trials, len(self.show_index))
        elif self._remaining_index:
            self._session_start_time = time.time()
            self._need_break = False
            self._run_batch()
        else:
            self._finish()

    def Resume(self):
        self._session_start_time = time.time()
        self._need_break = False
        self._run_batch()

    def _finish(self):
        if self._time_timer is not None:
            self._time_timer.stop()
        self.exp_finished.emit()

    def FinishExperiment(self, all_results):
        self.result = all_results
        if self.scoring_page is not None:
            self.scoring_page.hide()
            self.scoring_page.deleteLater()
            self.scoring_page = None
        self.exp_finished.emit()

    def GetResult(self):
        return self.result

    def GetShowIndex(self):
        return self.show_index

    def Release(self):
        self.scoring_page = None
