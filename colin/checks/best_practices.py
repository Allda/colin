import logging

from colin.core.checks.containers import ContainerCheck
from colin.core.checks.filesystem import FileSystemCheck
from colin.core.checks.images import ImageCheck
from colin.core.result import CheckResult

logger = logging.getLogger(__name__)


class CmdOrEntrypointCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super(CmdOrEntrypointCheck, self) \
            .__init__(name="cmd_or_entrypoint",
                      message="Cmd or Entrypoint has to be specified",
                      description="An ENTRYPOINT allows you to configure a container that will run as an executable. "
                                  "The main purpose of a CMD is to provide defaults for an executing container.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#CMD.2FENTRYPOINT_2",
                      tags=["cmd", "entrypoint"])

    def check(self, target):
        metadata = target.instance.get_metadata()["Config"]
        cmd_present = "Cmd" in metadata and metadata["Cmd"]
        msg_cmd_present = "Cmd {}specified.".format("" if cmd_present else "not ")
        logger.debug(msg_cmd_present)

        entrypoint_present = "Entrypoint" in metadata and metadata["Entrypoint"]
        msg_entrypoint_present = "Entrypoint {}specified.".format("" if entrypoint_present else "not ")
        logger.debug(msg_entrypoint_present)

        passed = cmd_present or entrypoint_present
        return CheckResult(ok=passed,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[msg_cmd_present, msg_entrypoint_present])


class HelpFileOrReadmeCheck(FileSystemCheck):

    def __init__(self):
        super(HelpFileOrReadmeCheck, self) \
            .__init__(name="help_file_or_readme",
                      message="The 'helpfile' has to be provided.",
                      description="Just like traditional packages, containers need "
                                  "some 'man page' information about how they are to be used,"
                                  " configured, and integrated into a larger stack.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#Help_File",
                      files=['/help.1', '/README.md'],
                      tags=['filesystem', 'helpfile', 'man'],
                      all_must_be_present=False)


class HelpFileCheck(FileSystemCheck):

    def __init__(self):
        super(HelpFileCheck, self) \
            .__init__(name="help_file_required",
                      message="The 'helpfile' has to be provided.",
                      description="Just like traditional packages, containers need "
                                  "some 'man page' information about how they are to be used,"
                                  " configured, and integrated into a larger stack.",
                      reference_url="https://fedoraproject.org/wiki/Container:Guidelines#Help_File",
                      files=['/help.1'],
                      tags=['filesystem', 'helpfile', 'man'],
                      all_must_be_present=False)


class NoRootCheck(ContainerCheck, ImageCheck):

    def __init__(self):
        super(NoRootCheck, self) \
            .__init__(name="no_root",
                      message="Service should not run as root by default.",
                      description="It can be insecure to run service as root.",
                      reference_url="?????",
                      tags=["root", "user"])

    def check(self, target):
        metadata = target.instance.get_metadata()["Config"]
        root_present = "User" in metadata and metadata["User"] in ["", "0", "root"]

        return CheckResult(ok=not root_present,
                           severity=self.severity,
                           description=self.description,
                           message=self.message,
                           reference_url=self.reference_url,
                           check_name=self.name,
                           logs=[])
