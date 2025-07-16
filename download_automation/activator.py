from .activator_utils import *

class Activator:
    def __init__(self):
        self.title = PROCESS_NAME
        print('|- setting initial configurations ...')
        wait_for_n_seconds(1)
        self.mos, self.bos = self.set_office_systems()
        self.set_canonical_settings()

    def set_office_systems(self):
        print('|- checking office system windows ...')
        windows_initial = get_operating_windows_by_title(self.title)
        running_systems_initial = assign_office_system_type(windows_initial)
        list_of_running_systems_initial = list(running_systems_initial.keys())
        if 'MOS' in list_of_running_systems_initial and 'BOS' in list_of_running_systems_initial:
            self.mos = running_systems_initial['MOS']
            self.bos = running_systems_initial['BOS']
        else:
            if 'MOS' not in list_of_running_systems_initial:
                print('|- (MOS) is not running.')
                mos_is_running = execute_system('MOS')
            else:
                mos_is_running = True
            if mos_is_running and 'BOS' not in list_of_running_systems_initial:
                print('|- (BOS) is not running.')
                bos_is_running = execute_system('BOS')
            else:
                bos_is_running = True
            if mos_is_running and bos_is_running:
                wait_for_n_seconds(5)
                windows = get_operating_windows_by_title(self.title)
                print('operating windows:', len(windows))
                running_systems = assign_office_system_type(windows)
                print(f'|- set (MOS).')
                self.mos = running_systems['MOS']
                print(f'|- set (BOS).')
                self.bos = running_systems['BOS']
        print('|- assigned: (MOS), (BOS) ')
        return self.mos, self.bos

    def set_canonical_settings(self):
        if hasattr(self, 'mos') and hasattr(self, 'bos'):
            print('|- setting canonical configurations ...')
        else:
            raise Exception('|- not assigned: (MOS), (BOS)')
        for window in [self.mos, self.bos]:
            set_default_setting(window)
        print('|- canonical settings complete.')
        return None

    def execute_mos(self):
        execute_system('MOS')
        return None
    
    def execute_bos(self):
        execute_system('BOS')
        return None

    def on_mos(self):
        print('|- on (MOS) ...')
        activate_window(self.mos)
        return None
    
    def on_bos(self):
        print('|- on (BOS) ...')
        activate_window(self.bos)
        return None
    
    def quit_all(self):
        close_system()
        return None
