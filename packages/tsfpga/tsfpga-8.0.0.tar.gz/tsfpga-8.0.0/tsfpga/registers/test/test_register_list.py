# --------------------------------------------------------------------------------------------------
# Copyright (c) Lukas Vik. All rights reserved.
#
# This file is part of the tsfpga project.
# https://tsfpga.com
# https://gitlab.com/tsfpga/tsfpga
# --------------------------------------------------------------------------------------------------

import copy
from pathlib import Path
import unittest
from unittest.mock import patch

import pytest

from tsfpga.system_utils import create_file
from tsfpga.registers.parser import from_toml
from tsfpga.registers.register import Register
from tsfpga.registers.register_list import RegisterList


def test_from_default_registers():
    register_a = Register(name="a", index=0, mode="r", description="AA")
    register_b = Register(name="b", index=1, mode="w", description="BB")
    default_registers = [register_a, register_b]

    register_list = RegisterList.from_default_registers(
        name="apa", source_definition_file=None, default_registers=default_registers
    )

    # Change some things in the register objects to show that they are copied
    default_registers.append(Register(name="c", index=2, mode="r_w", description="CC"))
    register_a.mode = "w"
    register_b.name = "x"

    assert len(register_list.register_objects) == 2
    assert register_list.get_register("a").mode == "r"
    assert register_list.get_register("b").name == "b"


@patch("tsfpga.registers.register_list.git_commands_are_available", autospec=True)
@patch("tsfpga.registers.register_list.get_git_commit", autospec=True)
@patch("tsfpga.registers.register_list.svn_commands_are_available", autospec=True)
@patch("tsfpga.registers.register_list.get_svn_revision_information", autospec=True)
def test_generated_source_info(
    get_svn_revision_information,
    svn_commands_are_available,
    get_git_commit,
    git_commands_are_available,
):
    source_definition_file = Path("/apa/whatever/regs.toml")
    register_list = RegisterList(name="a", source_definition_file=source_definition_file)
    expected_first_line = "This file is automatically generated by tsfpga."

    # Test with git information
    git_commands_are_available.return_value = True
    get_git_commit.return_value = "HASH"

    got = register_list.generated_source_info()
    assert got[0] == expected_first_line
    assert " from file regs.toml at commit HASH." in got[1]

    # Test with SVN information
    git_commands_are_available.return_value = False
    svn_commands_are_available.return_value = True
    get_svn_revision_information.return_value = "REVISION"

    got = register_list.generated_source_info()
    assert got[0] == expected_first_line
    assert " from file regs.toml at revision REVISION." in got[1]

    # Test with no source definition file
    register_list = RegisterList(name="a", source_definition_file=None)

    got = register_list.generated_source_info()
    assert got[0] == expected_first_line
    assert "from file" not in got[1]
    assert " at revision REVISION." in got[1]


def test_header_constants():
    registers = RegisterList(name="apa", source_definition_file=None)
    hest = registers.add_constant("hest", 123)
    zebra = registers.add_constant("zebra", 456, "description")

    assert len(registers.constants) == 2

    assert registers.get_constant("hest") == hest
    assert registers.get_constant("zebra") == zebra

    with pytest.raises(ValueError) as exception_info:
        assert registers.get_constant("non existing") is None
    assert (
        str(exception_info.value)
        == 'Could not find constant "non existing" within register list "apa"'
    )

    zebra.value = -5
    assert registers.get_constant("zebra").value == -5


def test_invalid_register_mode_should_raise_exception():
    registers = RegisterList(None, None)
    registers.append_register(name="test", mode="r_w", description="")

    with pytest.raises(ValueError) as exception_info:
        registers.append_register(name="hest", mode="x", description="")
    assert str(exception_info.value) == 'Invalid mode "x" for register "hest"'

    register_array = registers.append_register_array("array", 2, "")
    register_array.append_register(name="apa", mode="r", description="")
    with pytest.raises(ValueError) as exception_info:
        register_array.append_register(name="zebra", mode="y", description="")
    assert str(exception_info.value) == 'Invalid mode "y" for register "zebra"'


def test_registers_are_appended_properly_and_can_be_edited_in_place():
    register_array = RegisterList(name="apa", source_definition_file=Path("."))

    register_hest = register_array.append_register(name="hest", mode="r", description="")
    assert register_hest.index == 0

    register_zebra = register_array.append_register(name="zebra", mode="r", description="")
    assert register_zebra.index == 1

    register_hest.description = "new desc"
    assert register_array.register_objects[0].description == "new desc"


def test_register_arrays_are_appended_properly_and_can_be_edited_in_place():
    register_array = RegisterList(name="apa", source_definition_file=Path("."))

    register_array_hest = register_array.append_register_array(
        name="hest", length=4, description=""
    )
    assert register_array_hest.base_index == 0
    register_array_hest.append_register(name="foo", mode="r", description="")
    register_array_hest.append_register(name="bar", mode="w", description="")

    register_array_zebra = register_array.append_register_array(
        name="zebra", length=2, description=""
    )
    assert register_array_zebra.base_index == 8


def test_get_register():
    register_list = RegisterList(name="apa", source_definition_file=None)
    hest = register_list.append_register(name="hest", mode="r", description="")
    zebra = register_list.append_register(name="zebra", mode="r", description="")
    register_list.append_register_array(name="register_array", length=3, description="")

    assert register_list.get_register("hest") is hest
    assert register_list.get_register("zebra") is zebra

    with pytest.raises(ValueError) as exception_info:
        assert register_list.get_register("non existing") is None
    assert (
        str(exception_info.value)
        == 'Could not find register "non existing" within register list "apa"'
    )

    with pytest.raises(ValueError) as exception_info:
        assert register_list.get_register("register_array") is None
    assert (
        str(exception_info.value)
        == 'Could not find register "register_array" within register list "apa"'
    )
    register_list.get_register_array("register_array")


def test_get_register_array():
    register_list = RegisterList(name="apa", source_definition_file=None)
    hest = register_list.append_register_array(name="hest", length=3, description="")
    zebra = register_list.append_register_array(name="zebra", length=2, description="")
    register_list.append_register(name="register", mode="r", description="")

    assert register_list.get_register_array("hest") is hest
    assert register_list.get_register_array("zebra") is zebra

    with pytest.raises(ValueError) as exception_info:
        assert register_list.get_register_array("non existing") is None
    assert (
        str(exception_info.value)
        == 'Could not find register array "non existing" within register list "apa"'
    )

    with pytest.raises(ValueError) as exception_info:
        assert register_list.get_register_array("register") is None
    assert (
        str(exception_info.value)
        == 'Could not find register array "register" within register list "apa"'
    )
    register_list.get_register("register")


def test_get_register_index():
    register_list = RegisterList(name=None, source_definition_file=None)

    register_list.append_register(name="apa", mode="r", description="")
    register_list.append_register(name="hest", mode="r", description="")

    zebra = register_list.append_register_array(name="zebra", length=2, description="")
    zebra.append_register(name="bar", mode="r", description="")
    zebra.append_register(name="baz", mode="r", description="")

    assert register_list.get_register_index(register_name="apa") == 0
    assert register_list.get_register_index(register_name="hest") == 1
    assert (
        register_list.get_register_index(
            register_name="bar", register_array_name="zebra", register_array_index=0
        )
        == 2
    )
    assert (
        register_list.get_register_index(
            register_name="baz", register_array_name="zebra", register_array_index=1
        )
        == 5
    )


def test_repr_basic():
    # Check that repr is an actual representation, not just "X object at 0xABCDEF"
    assert "apa" in repr(RegisterList(name="apa", source_definition_file=Path(".")))

    # Different name
    assert repr(RegisterList(name="apa", source_definition_file=Path("."))) != repr(
        RegisterList(name="hest", source_definition_file=Path("."))
    )

    # Different source_definition_file
    assert repr(RegisterList(name="apa", source_definition_file=Path("."))) != repr(
        RegisterList(name="apa", source_definition_file=Path("./zebra"))
    )


def test_repr_with_constant_added():
    register_list_a = RegisterList(name="apa", source_definition_file=Path("."))
    register_list_b = RegisterList(name="apa", source_definition_file=Path("."))
    assert repr(register_list_a) == repr(register_list_b)

    register_list_a.add_constant(name="zebra", value=3)

    assert repr(register_list_a) != repr(register_list_b)


def test_repr_with_register_appended():
    register_list_a = RegisterList(name="apa", source_definition_file=Path("."))
    register_list_b = RegisterList(name="apa", source_definition_file=Path("."))
    assert repr(register_list_a) == repr(register_list_b)

    register_list_a.append_register(name="zebra", mode="w", description="")

    assert repr(register_list_a) != repr(register_list_b)


def test_repr_with_register_array_appended():
    register_list_a = RegisterList(name="apa", source_definition_file=Path("."))
    register_list_b = RegisterList(name="apa", source_definition_file=Path("."))
    assert repr(register_list_a) == repr(register_list_b)

    register_list_a.append_register_array(name="zebra", length=4, description="")

    assert repr(register_list_a) != repr(register_list_b)


def test_deep_copy_of_register_list_actually_copies_everything():
    original_list = RegisterList("original", Path("/original_file.txt"))
    original_list.add_constant("original_constant", value=2, description="original constant")
    original_list.append_register("original_register", "w", description="original register")
    original_array = original_list.append_register_array("original_array", length=4, description="")
    original_array.append_register(name="original_register_in_array", mode="r", description="")

    copied_list = copy.deepcopy(original_list)

    assert copied_list.constants is not original_list.constants
    assert copied_list.constants[0] is not original_list.constants[0]

    copied_list.add_constant(name="new_constant", value=5)
    assert len(copied_list.constants) == 2 and len(original_list.constants) == 1

    assert copied_list.register_objects is not original_list.register_objects
    assert copied_list.register_objects[0] is not original_list.register_objects[0]

    # Original register in position 0, original register array in position 1, new register in 2
    copied_list.append_register(name="new_register", mode="r", description="")
    assert len(copied_list.register_objects) == 3 and len(original_list.register_objects) == 2

    assert copied_list.register_objects[1] is not original_list.register_objects[1]
    assert (
        copied_list.register_objects[1].registers is not original_list.register_objects[1].registers
    )
    assert (
        copied_list.register_objects[1].registers[0]
        is not original_list.register_objects[1].registers[0]
    )
    copied_list.register_objects[1].append_register(
        name="new_register_in_array", mode="r_w", description=""
    )
    assert len(copied_list.register_objects[1].registers) == 2
    assert len(original_list.register_objects[1].registers) == 1


# pylint: disable=too-many-public-methods
@pytest.mark.usefixtures("fixture_tmp_path")
class TestRegisterList(unittest.TestCase):

    tmp_path = None

    module_name = "sensor"
    toml_data = """\
################################################################################
[register.data]

mode = "w"
description = "My register"

"""

    def setUp(self):
        self.toml_file = self.create_toml_file_with_extras()

    def create_toml_file_with_extras(self, toml_extras=""):
        data = self.toml_data + toml_extras
        return create_file(self.tmp_path / "sensor_regs.toml", data)

    def test_create_vhdl_package_should_not_run_if_nothing_has_changed(self):
        register_list = from_toml(self.module_name, self.toml_file)
        register_list.add_constant(name="apa", value=3)
        register_list.create_vhdl_package(self.tmp_path)

        register_list = from_toml(self.module_name, self.toml_file)
        register_list.add_constant(name="apa", value=3)
        with patch(
            "tsfpga.registers.register_list.RegisterList._create_vhdl_package", autospec=True
        ) as mocked_create_vhdl_package:
            register_list.create_vhdl_package(self.tmp_path)
            mocked_create_vhdl_package.assert_not_called()

    def test_create_vhdl_package_should_run_if_hash_or_version_can_not_be_read(self):
        register_list = from_toml(self.module_name, self.toml_file)
        register_list.create_vhdl_package(self.tmp_path)

        # Overwrite the generated file, without a valid header
        vhd_file = self.tmp_path / "sensor_regs_pkg.vhd"
        assert vhd_file.exists()
        create_file(vhd_file, contents="-- Mumbo jumbo\n")

        register_list = from_toml(self.module_name, self.toml_file)
        with patch(
            "tsfpga.registers.register_list.RegisterList._create_vhdl_package", autospec=True
        ) as mocked_create_vhdl_package:
            register_list.create_vhdl_package(self.tmp_path)
            mocked_create_vhdl_package.assert_called_once()

    def test_create_vhdl_package_should_run_again_if_toml_file_has_changed(self):
        register_list = from_toml(self.module_name, self.toml_file)
        register_list.create_vhdl_package(self.tmp_path)

        self.create_toml_file_with_extras(
            """
[constant.apa]

value = 3
"""
        )
        register_list = from_toml(self.module_name, self.toml_file)
        with patch(
            "tsfpga.registers.register_list.RegisterList._create_vhdl_package", autospec=True
        ) as mocked_create_vhdl_package:
            register_list.create_vhdl_package(self.tmp_path)
            mocked_create_vhdl_package.assert_called_once()

    def test_create_vhdl_package_should_run_again_if_list_is_modified(self):
        register_list = from_toml(self.module_name, self.toml_file)
        register_list.create_vhdl_package(self.tmp_path)

        register_list = from_toml(self.module_name, self.toml_file)
        register_list.add_constant(name="apa", value=3)
        with patch(
            "tsfpga.registers.register_list.RegisterList._create_vhdl_package", autospec=True
        ) as mocked_create_vhdl_package:
            register_list.create_vhdl_package(self.tmp_path)
            mocked_create_vhdl_package.assert_called_once()

    def test_create_vhdl_package_should_run_again_if_version_is_changed(self):
        register_list = from_toml(self.module_name, self.toml_file)
        register_list.create_vhdl_package(self.tmp_path)

        with patch(
            "tsfpga.registers.register_list.RegisterList._create_vhdl_package", autospec=True
        ) as mocked_create_vhdl_package, patch(
            "tsfpga.registers.register_list.__version__", autospec=True
        ) as _:
            register_list.create_vhdl_package(self.tmp_path)
            mocked_create_vhdl_package.assert_called_once()
