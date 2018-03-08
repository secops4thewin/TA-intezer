
# encoding = utf-8
# Always put this line at the beginning of this file
import ta_intezer_declare

import os
import sys

from alert_actions_base import ModularAlertBase
import modalert_intezer_sha256_check_helper

class AlertActionWorkerintezer_sha256_check(ModularAlertBase):

    def __init__(self, ta_name, alert_name):
        super(AlertActionWorkerintezer_sha256_check, self).__init__(ta_name, alert_name)

    def validate_params(self):

        if not self.get_global_setting("api_key"):
            self.log_error('api_key is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_global_setting("index"):
            self.log_error('index is a mandatory setup parameter, but its value is None.')
            return False

        if not self.get_param("sha_256_hash"):
            self.log_error('sha_256_hash is a mandatory parameter, but its value is None.')
            return False

        if not self.get_param("search_description"):
            self.log_error('search_description is a mandatory parameter, but its value is None.')
            return False
        return True

    def process_event(self, *args, **kwargs):
        status = 0
        try:
            if not self.validate_params():
                return 3
            status = modalert_intezer_sha256_check_helper.process_event(self, *args, **kwargs)
        except (AttributeError, TypeError) as ae:
            self.log_error("Error: {}. Please double check spelling and also verify that a compatible version of Splunk_SA_CIM is installed.".format(ae.message))
            return 4
        except Exception as e:
            msg = "Unexpected error: {}."
            if e.message:
                self.log_error(msg.format(e.message))
            else:
                import traceback
                self.log_error(msg.format(traceback.format_exc()))
            return 5
        return status

if __name__ == "__main__":
    exitcode = AlertActionWorkerintezer_sha256_check("TA-intezer", "intezer_sha256_check").run(sys.argv)
    sys.exit(exitcode)
