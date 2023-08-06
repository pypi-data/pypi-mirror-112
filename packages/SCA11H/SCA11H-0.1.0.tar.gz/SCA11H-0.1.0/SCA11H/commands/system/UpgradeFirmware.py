from SCA11H.commands.base.PostCommand import PostCommand, PostResult

import json


class UpgradeFirmware(PostCommand):
    """ System Upgrade Firmware """

    def __init__(self, image: str, reboot: bool, **kwargs):
        super().__init__(endpoint='/sys/fwupd',
                         payload=json.dumps({"image": image}),
                         **kwargs)

        # Note: After ”System Upgrade Firmware” command is completed, a separate reboot command is required to
        # activate the new firmware. BSN will run the old firmware until reboot.
        self.reboot = reboot

    def run(self, checked: bool = True, **kwargs) -> PostResult:
        res = self.run_for_plaintext_result()
        if res == 'success':
            res = PostResult(payload={'error': 0})
            if self.reboot:
                from SCA11H.commands.system.RunCommand import RunCommand, Command
                res = RunCommand(command=Command.Reboot).run()
        else:
            res = PostResult(payload={'error': -1})

        return res

    # TODO: Add command-line support
