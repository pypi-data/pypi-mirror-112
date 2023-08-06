# -*- coding: utf-8 -*-
# dreamtools/logmng.py

import logging
import logging.config as log_config

from . import profiler
from . import tools
from .cfgmng import CFGBases


class CReponder:
    def __init__(self, status=200, data=None, msg=None):
        """ Constructeur de class

        :type status: int, default 200
        :param data: données renvoyée
        :param msg: message associée à la réponse

        """
        self.status = status
        self.data = data
        self.message = msg

    def __call__(self, status, data=None, msg=None):
        self.status = status
        self.data = data
        self.message = msg

    @property
    def ok(self):
        """ Renvoie le status de la réponse

        :rtype: bool
        """
        return 200 <= self._status < 300

    @property
    def response(self):
        """
        :return: {"message": self.message, "data": self.data, 'status_code': self._status}
        """
        return {"message": self.message, "data": self.data, 'status_code': self._status}

    @property
    def status(self):
        return self._status

    @property
    def data(self):
        return self._data

    @property
    def message(self):
        return self._msg

    @status.setter
    def status(self, v):
        self._status = v

    @message.setter
    def message(self, v):
        self._msg = v

    @data.setter
    def data(self, v):
        self._data = v


class CError(Exception, CReponder):
    """ Gestion des erreurs et traitement des exceptions personnalisées """

    def __init__(self, message, status, title='ERRCustom'):
        """
        :param int status: status code
        :param str message: message d'erreur
        :param str title: titre

        """
        Exception.__init__(self, message)
        CReponder.__init__(self, status, msg=message)

        self.title = title


class CTracker:
    tracker = None
    LOG_TRACKED = ''

    @classmethod
    def config(cls, mode='PRODUCTION'):
        """Initialisation du gestionnaire de log à partir de la configuration enregistré

        .. warning::
            La configuration doit être configurer dans le fichier <PROJECT_DIR>/cdg/.log.yml

        :Exemple:cls
            >>> CTracker.config()
            Configuration mode PRODUCTION
            >>> CTracker.config("DEBUG")
            Configuration mode debug

        """
        try:
            profiler.makedirs(profiler.path_build(tools.PROJECT_DIR, 'logs'))
            log_config.dictConfig(CFGBases.logs_cfg())
            cls.tracker = logging.getLogger(mode)
        except Exception as e:
            tools.print_err(e, ': ', 'Error in Logging Configuration. Using default configs')
            logging.basicConfig(level=logging.NOTSET)

    @classmethod
    def msg_tracking(cls, msg, title, log_level=logging.INFO, code=0):
        """ Tracking message

        :param str msg: message à ecrire dans logs
        :param str title: Titre ou référence associé au message
        :param int log_level: LOG LEVEL Niveau de l'alert (DEBUG | INFO | WARN | )
        :param int code: Code numérique

        """
        cls.tracker.log(log_level, msg, extra={'title': title, 'code': code})

    @classmethod
    def alert_tracking(cls, msg, title, code=0):
        """ Message d'alerte (WARNING)

        :param str msg: message à ecrire dans logs
        :param str title: Titre ou référence associé au message
        :param int code: Code numérique
        """

        cls.msg_tracking(msg, title, logging.WARNING, code)

    @classmethod
    def info_tracking(cls, msg, title, code=0):
        """ Message d'info (INFO)

        :param str msg: message à ecrire dans logs
        :param str title: Titre ou référence associé au message
        :param code: Code numérique
        """

        cls.msg_tracking(msg, title, logging.INFO, code)

    @classmethod
    def error_tracking(cls, msg, title, code=500):
        """ Message d'error (ERROR)

        :param str msg: message à ecrire dans logs
        :param str title: Titre ou référence associé au message
        :param int code: Code numérique
        """

        cls.msg_tracking(msg, title, logging.ERROR, code)

    @classmethod
    def critical_tracking(cls, msg, title, code=0):
        """ Message dcritique (CRITIQUE)

        :param str msg: message à ecrire dans logs
        :param str title: Titre ou référence associé au message
        :param int code: Code numérique
        """
        cls.msg_tracking(msg, title, logging.CRITICAL, code)

    @classmethod
    def flag(cls, trace):
        """ Permet de pointer la dernier action

        :param str trace: Action à enregistrer
        """
        cls.LOG_TRACKED = trace

    @classmethod
    def exception_tracking(cls, ex, title, status=500):
        """
        Récupération et traitement des exceptions

        :param ex: Exception
        :param str title: Information
        """

        try:
            if cls.LOG_TRACKED != '':
                cls.msg_tracking(cls.LOG_TRACKED, title, logging.INFO)
                cls.LOG_TRACKED = ''
        except :
            pass

        try:
            if isinstance(ex, CError):
                cls.error_tracking(ex.message, ex.title, code=ex.status or status)
                return ex
            else:
                cls.error_tracking(ex.__str__(), title)
                return CError(ex.__str__(), status, title)
        except Exception as sex:
            tools.print_err('*****************  Erreur systeme *****************: \n', sex)
            tools.print_err('** Erreur interceptée : ', ex)

            return CError(ex, status=status)

    @classmethod
    def fntracker(cls, fn, action, *args, **kwargs):
        """ Execution "securisé" d'une fonction avec gestions des erreurs
        
        :param fn: fonction a executer
        :param action: Titre de l'execution pour tracabilité
        :param args: argument de la fonction
        :param kwargs: parametres supplementaire (status par defaut en cas de reussite)
        :rtype: CReponder

        :Exemple:
            >>> from dreamtools.logmng import CTracker
            >>> def fn(arg)::
            >>>     return int(arg)
            >>> r = CTracker.fntracker(fn, 'Test de convertion int', 'j')
            >>> r.response
            {'message': "invalid literal for int() with base 10: 'j'", 'data': None, 'status_code': 500}
            >>> r = CTracker.fntracker(fn, 'Test de convertion int', '589321')
            >>> r.response
            {'message': None, 'data': 589321, 'status_code': 200}
        """

        try:
            cls.flag('{}'.format(action))
            status = kwargs.get('status', 200)

            if kwargs.get('status'): del kwargs['status']
            r = fn(*args, **kwargs)

            return r if isinstance(r, CReponder) else CReponder(status, r)

        except Exception as ex:
            return cls.exception_tracking(ex, action)
