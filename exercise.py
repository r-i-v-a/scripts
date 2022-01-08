#!/usr/bin/env python3

import random

exercise_list = [
	"A",
	"B",
	"C",
	"D",
	"E"
]

# Build a workflow.
#
# wf             workflow name
# classpath      java classpath needed for running compilation
# folder         destination folder on the platform
def build_test(tname, project, folder, version_id, compiler_flags):
    desc = test_files[tname]
    print("build {} {}".format(desc.kind, desc.name))
    print("Compiling {} to a {}".format(desc.source_file, desc.kind))
    # both static and dynamic instance type selection should work,
    # so we can test them at random
    instance_type_selection = random.choice(["static", "dynamic"])
    cmdline = [
        "java",
        "-jar",
        os.path.join(top_dir, "dxCompiler-{}.jar".format(version_id)),
        "compile",
        desc.source_file,
        "-force",
        "-folder",
        folder,
        "-project",
        project.get_id(),
        "-instanceTypeSelection",
        instance_type_selection
    ]
    if "manifest" in desc.source_file:
        cmdline.append("-useManifests")
    cmdline += compiler_flags
    print(" ".join(cmdline))
    try:
        oid = subprocess.check_output(cmdline).strip()
    except subprocess.CalledProcessError as cpe:
        print(f"error compiling {desc.source_file}\n  stdout: {cpe.stdout}\n  stderr: {cpe.stderr}")
        raise
    return oid.decode("ascii")


def ensure_dir(path):
    print("making sure that {} exists".format(path))
    if not os.path.exists(path):
        os.makedirs(path)


def wait_for_completion(test_exec_objs):
    print("awaiting completion ...")
    successes = []
    failures = []
    for i, exec_obj in test_exec_objs:
        tname = find_test_from_exec(exec_obj)
        desc = test_files[tname]
        try:
            exec_obj.wait_on_done()
            print("Analysis {}.{} succeeded".format(desc.name, i))
            successes.append((i, exec_obj, True))
        except DXJobFailureError:
            if tname in expected_failure or "{}.{}".format(tname, i) in expected_failure:
                print("Analysis {}.{} failed as expected".format(desc.name, i))
                successes.append((i, exec_obj, False))
            else:
                cprint("Error: analysis {}.{} failed".format(desc.name, i), "red")
                failures.append((tname, exec_obj))
    print("tools execution completed")
    return successes, failures


# Run [workflow] on several inputs, return the analysis ID.
def run_executable(
    project, test_folder, tname, oid, debug_flag, delay_workspace_destruction, instance_type=default_instance_type
):
    desc = test_files[tname]

    def once(i):
        try:
            if tname in test_defaults or i < 0:
                print("  with empty input")
                inputs = {}
            else:
                print("  with input file: {}".format(desc.dx_input[i]))
                inputs = read_json_file(desc.dx_input[i])
            project.new_folder(test_folder, parents=True)
            if desc.kind == "workflow":
                exec_obj = dxpy.DXWorkflow(project=project.get_id(), dxid=oid)
                run_kwargs = {"ignore_reuse_stages": ["*"]}
            elif desc.kind == "applet":
                exec_obj = dxpy.DXApplet(project=project.get_id(), dxid=oid)
                run_kwargs = {"ignore_reuse": True}
            else:
                raise RuntimeError("Unknown kind {}".format(desc.kind))

            if debug_flag:
                run_kwargs["debug"] = {
                    "debugOn": ["AppError", "AppInternalError", "ExecutionError"]
                }
                run_kwargs["allow_ssh"] = ["*"]

            if delay_workspace_destruction:
                run_kwargs["delay_workspace_destruction"] = True
            if instance_type:
                run_kwargs["instance_type"] = instance_type

            return exec_obj.run(
                inputs,
                project=project.get_id(),
                folder=test_folder,
                name="{} {}".format(desc.name, git_revision),
                **run_kwargs,
            )
        except Exception as e:
            print("exception message={}".format(e))
            return None

    def run(i):
        for _ in range(1, 5):
            retval = once(i)
            if retval is not None:
                return retval
            print("Sleeping for 5 seconds before trying again")
            time.sleep(5)
        else:
            raise RuntimeError("running workflow")

    n = len(desc.dx_input)
    if n == 0:
        return [(0, run(-1))]
    else:
        return [(i, run(i)) for i in range(n)]


def extract_outputs(tname, exec_obj) -> dict:
    desc = test_files[tname]
    if desc.kind == "workflow":
        locked = tname not in test_unlocked
        if locked:
            return exec_obj["output"]
        else:
            stages = exec_obj["stages"]
            for snum in range(len(stages)):
                crnt = stages[snum]
                if crnt["id"] == "stage-outputs":
                    return stages[snum]["execution"]["output"]
            raise RuntimeError(
                "Analysis for test {} does not have stage 'outputs'".format(tname)
            )
    elif desc.kind == "applet":
        return exec_obj["output"]
    else:
        raise RuntimeError("Unknown kind {}".format(desc.kind))


def run_test_subset(
    project, runnable, test_folder, debug_flag, delay_workspace_destruction, delay_run_errors
):
    # Run the workflows
    test_exec_objs = []
    errors = [] if delay_run_errors else None
    for tname, oid in runnable.items():
        desc = test_files[tname]
        print("Running {} {} {}".format(desc.kind, desc.name, oid))
        if tname in test_instance_type:
            instance_type = None
        else:
            instance_type = default_instance_type
        try:
            anl = run_executable(
                project, test_folder, tname, oid, debug_flag, delay_workspace_destruction, instance_type
            )
            test_exec_objs.extend(anl)
        except Exception as ex:
            if tname in test_compilation_failing:
                cprint("Workflow {} execution failed as expected".format(tname))
                continue
            elif delay_run_errors:
                cprint(f"Workflow {tname} execution failed", "red")
                traceback.print_exc()
                errors.append(tname)
            else:
                raise ex

    if errors:
        write_failed(errors)
        raise RuntimeError(f"failed to run one or more tests {','.join(errors)}")

    print("executions: " + ", ".join([a[1].get_id() for a in test_exec_objs]))

    # Wait for completion
    successful_executions, failed_executions = wait_for_completion(test_exec_objs)

    print("Verifying results")

    def verify_test(exec_obj, i):
        exec_desc = exec_obj.describe()
        tname = find_test_from_exec(exec_obj)
        test_desc = test_files[tname]
        try:
            exec_outputs = extract_outputs(tname, exec_desc)
        except:
            if tname in expected_failure or "{}.{}".format(tname, i) in expected_failure:
                print("Analysis {}.{} failed as expected".format(tname, i))
                return None
            else:
                raise
        if len(test_desc.results) > i:
            shouldbe = read_json_file_maybe_empty(test_desc.results[i])
            correct = True
            print("Checking results for workflow {} job {}".format(test_desc.name, i))
            for key, expected_val in shouldbe.items():
                if not validate_result(tname, exec_outputs, key, expected_val, project):
                    correct = False
                    break
            if correct:
                if tname in expected_failure or "{}.{}".format(tname, i) in expected_failure:
                    cprint(
                        "Error: analysis {}.{} was expected to fail but its results are valid".format(test_desc.name, i),
                        "red"
                    )
                    return tname
                else:
                    print("Analysis {}.{} results are valid".format(test_desc.name, i))
                    return None
            else:
                if tname in expected_failure or "{}.{}".format(tname, i) in expected_failure:
                    print("Analysis {}.{} results are invalid as expected".format(test_desc.name, i))
                    return None
                else:
                    cprint("Error: analysis {}.{} results are invalid".format(test_desc.name, i), "red")
                    return tname

    failed_verifications = []
    for i, exec_obj, verify in successful_executions:
        if verify:
            failed_name = verify_test(exec_obj, i)
            if failed_name is not None:
                failed_verifications.append(failed_name)

    print("-----------------------------")
    print(f"Total tests: {len(test_exec_objs)}")

    if failed_executions or failed_verifications:
        failed_tools = set(e[0] for e in failed_executions)
        unverified_tools = set(failed_verifications)
        if failed_executions:
            fexec = "\n".join(failed_tools)
            print(f"Failed executions: {len(failed_executions)}")
            print(f"Tools failed execution:\n{fexec}")
        if failed_verifications:
            fveri = "\n".join(unverified_tools)
            print(f"Failed verifications: {len(failed_verifications)}")
            print(f"Tools failed results verification:\n{fveri}")
        write_failed(failed_tools | unverified_tools)
        raise RuntimeError("Failed")
    else:
        print("All tests successful!")


def write_failed(failed):
    # write failed tests to a file so we can easily re-run them next time
    # if a .failed file already exists, make a backup
    if os.path.exists(".failed"):
        bak_file = ".failed.bak"
        i = 0
        while os.path.exists(bak_file):
            bak_file = f".failed.bak.{i}"
            i += 1
        shutil.copy(".failed", bak_file)
    with open(".failed", "wt") as out:
        failed_sorted = sorted(set(tname.split(".")[0] for tname in failed))
        out.write("\n".join(failed_sorted))


def print_test_list():
    test_list = "\n  ".join(sorted(key for key in test_files.keys()))
    print("List of tests:\n  {}".format(test_list))


# Choose set set of tests to run
def choose_tests(name):
    if name in test_suites.keys():
        return test_suites[name]
    if name == "All":
        return test_files.keys()
    if name in test_files.keys():
        return [name]
    # Last chance: check if the name is a prefix.
    # Accept it if there is exactly a single match.
    matches = [key for key in test_files.keys() if key.startswith(name)]
    if len(matches) > 1:
        raise RuntimeError(
            "Too many matches for test prefix {} -> {}".format(name, matches)
        )
    if len(matches) == 0:
        raise RuntimeError("Test prefix {} is unknown".format(name))
    return matches


# Find all the WDL test files, these are located in the 'test'
# directory. A test file must have some support files.
def register_all_tests(verbose: bool) -> None:
    for root, dirs, files in os.walk(test_dir):
        if os.path.basename(root).endswith("_ignore") or os.path.basename(root).endswith("_notimplemented"):
            continue
        for t_file in files:
            if t_file.endswith(".wdl") or t_file.endswith(".cwl"):
                base = os.path.basename(t_file)
                (fname, ext) = os.path.splitext(base)
            elif t_file.endswith(".cwl.json"):
                base = os.path.basename(t_file)
                fname = base[:-9]
                ext = ".cwl.json"
            else:
                continue

            if fname.startswith("library_"):
                continue
            if fname.endswith("_extern"):
                continue
            try:
                register_test(root, fname, ext)
            except Exception as e:
                if verbose:
                    print("Skipping file {} error={}".format(fname, e))


# Some compiler flags are test specific
def compiler_per_test_flags(tname):
    flags = []
    desc = test_files[tname]
    if tname not in test_unlocked:
        flags.append("-locked")
    if tname in test_reorg:
        flags.append("-reorg")
    if tname in test_project_wide_reuse:
        flags.append("-projectWideReuse")
    if tname in test_separate_outputs:
        flags.append("-separateOutputs")
    if tname in test_defaults and len(desc.raw_input) > 0:
        flags.append("-defaults")
        flags.append(desc.raw_input[0])
    if tname in test_upload_wait:
        flags.append("-waitOnUpload")
    else:
        for i in desc.raw_input:
            flags.append("-inputs")
            flags.append(i)
    if desc.extras is not None:
        flags += ["--extras", os.path.join(top_dir, desc.extras)]
    if tname in test_import_dirs:
        flags += ["--imports", os.path.join(top_dir, "test/imports/lib")]
    return flags


# Which project to use for a test
# def project_for_test(tname):

######################################################################


def native_call_dxni(project, applet_folder, version_id, verbose: bool):
    # build WDL wrapper tasks in test/dx_extern.wdl
    cmdline_common = [
        "java",
        "-jar",
        os.path.join(top_dir, "dxCompiler-{}.jar".format(version_id)),
        "dxni",
        "-force",
        "-folder",
        applet_folder,
        "-project",
        project.get_id(),
    ]
    if verbose:
        cmdline_common.append("--verbose")

    # draft-2 is not currently supported
    #     cmdline_draft2 = cmdline_common + [ "--language", "wdl_draft2",
    #                                         "--output", os.path.join(top_dir, "test/draft2/dx_extern.wdl")]
    #     print(" ".join(cmdline_draft2))
    #     subprocess.check_output(cmdline_draft2)

    cmdline_v1 = cmdline_common + [
        "-language",
        "wdl_v1.0",
        "-output",
        os.path.join(top_dir, "test/wdl_1_0/dx_extern.wdl"),
    ]
    print(" ".join(cmdline_v1))
    subprocess.check_output(cmdline_v1)


def dxni_call_with_path(project, path, version_id, verbose):
    # build WDL wrapper tasks in test/dx_extern.wdl
    cmdline = [
        "java",
        "-jar",
        os.path.join(top_dir, "dxCompiler-{}.jar".format(version_id)),
        "dxni",
        "-force",
        "-path",
        path,
        "-language",
        "wdl_v1.0",
        "-output",
        os.path.join(top_dir, "test/wdl_1_0/dx_extern_one.wdl"),
    ]
    if project is not None:
        cmdline.extend(["-project", project.get_id()])
    if verbose:
        cmdline.append("-verbose")
    print(" ".join(cmdline))
    subprocess.check_output(cmdline)


# Set up the native calling tests
def native_call_setup(project, applet_folder, version_id, verbose):
    native_applets = [
        "native_concat",
        "native_diff",
        "native_mk_list",
        "native_sum",
        "native_sum_012",
    ]

    # build the native applets, only if they do not exist
    for napl in native_applets:
        applet = list(
            dxpy.bindings.search.find_data_objects(
                classname="applet",
                name=napl,
                folder=applet_folder,
                project=project.get_id(),
            )
        )
        if len(applet) == 0:
            cmdline = [
                "dx",
                "build",
                os.path.join(top_dir, "test/applets/{}".format(napl)),
                "--destination",
                (project.get_id() + ":" + applet_folder + "/"),
            ]
            print(" ".join(cmdline))
            subprocess.check_output(cmdline)

    dxni_call_with_path(project, applet_folder + "/native_concat", version_id, verbose)
    native_call_dxni(project, applet_folder, version_id, verbose)

    # check if providing an applet-id in the path argument works
    first_applet = native_applets[0]
    results = dxpy.bindings.search.find_one_data_object(
        classname="applet",
        name=first_applet,
        folder=applet_folder,
        project=project.get_id(),
    )
    if results is None:
        raise RuntimeError("Could not find applet {}".format(first_applet))
    dxni_call_with_path(project, results["id"], version_id, verbose)


def native_call_app_setup(version_id, verbose):
    app_name = "native_hello"

    # Check if they already exist
    apps = list(dxpy.bindings.search.find_apps(name=app_name))
    if len(apps) == 0:
        # build the app
        cmdline = [
            "dx",
            "build",
            "--create-app",
            "--publish",
            os.path.join(top_dir, "test/apps/{}".format(app_name)),
        ]
        print(" ".join(cmdline))
        subprocess.check_output(cmdline)

    # build WDL wrapper tasks in test/dx_extern.wdl
    header_file = os.path.join(top_dir, "test/wdl_1_0/dx_app_extern.wdl")
    cmdline = [
        "java",
        "-jar",
        os.path.join(top_dir, "dxCompiler-{}.jar".format(version_id)),
        "dxni",
        "-apps",
        "only",
        "-force",
        "-language",
        "wdl_v1.0",
        "-output",
        header_file,
    ]
    if verbose:
        cmdline.append("--verbose")
    print(" ".join(cmdline))
    subprocess.check_output(cmdline)

    # check if providing an app-id in the path argument works
    results = dxpy.bindings.search.find_one_app(
        name=app_name, zero_ok=True, more_ok=False
    )
    if results is None:
        raise RuntimeError("Could not find app {}".format(app_name))
    dxni_call_with_path(None, results["id"], version_id, verbose)


######################################################################
# Compile the WDL files to dx:workflows and dx:applets
# delay_compile_errors: whether to aggregate all compilation errors
#   and only raise an Exception after trying to compile all the tests
def compile_tests_to_project(
    trg_proj,
    test_names,
    applet_folder,
    compiler_flags,
    version_id,
    lazy_flag,
    delay_compile_errors=False,
):
    runnable = {}
    errors = [] if delay_compile_errors else None
    for tname in test_names:
        specific_applet_folder = "{}/{}".format(applet_folder, tname)
        oid = None
        if lazy_flag:
            oid = lookup_dataobj(tname, trg_proj, specific_applet_folder)
        if oid is None:
            c_flags = compiler_flags[:] + compiler_per_test_flags(tname)
            try:
                oid = build_test(tname, trg_proj, specific_applet_folder, version_id, c_flags)
            except subprocess.CalledProcessError:
                if tname in test_compilation_failing:
                    print("Workflow {} compilation failed as expected".format(tname))
                    continue
                elif delay_compile_errors:
                    cprint(f"Workflow {tname} compilation failed", "red")
                    traceback.print_exc()
                    errors.append(tname)
                else:
                    raise
        runnable[tname] = oid
        print("runnable({}) = {}".format(tname, oid))
    if errors:
        write_failed(errors)
        raise RuntimeError(f"failed to compile one or more tests: {','.join(errors)}")
    return runnable


def main():
    global test_unlocked
    argparser = argparse.ArgumentParser(
        description="Run WDL compiler tests on the platform"
    )
    argparser.add_argument(
        "--archive", help="Archive old applets", action="store_true", default=False
    )
    argparser.add_argument(
        "--build",
        help="force: remove existing dxCompiler JAR and rebuild; only: only build dxCompiler, "
             "do not run any tests; if not specified, dxCompiler will be built only if there is "
             "not already a dxCompiler asset in the project",
        default=None
    )
    argparser.add_argument(
        "--compile-only",
        help="Only compile the workflows, don't run them",
        action="store_true",
        default=False,
    )
    argparser.add_argument("--compile-mode", help="Compilation mode")
    argparser.add_argument(
        "--debug",
        help="Run applets with debug-hold, and allow ssh",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--delay-workspace-destruction",
        help="Run applets with delayWorkspaceDestruction",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--force",
        help="Remove old versions of applets and workflows",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--folder", help="Use an existing folder, instead of building dxCompiler"
    )
    argparser.add_argument(
        "--lazy",
        help="Only compile workflows that are unbuilt",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--list",
        "--test-list",
        help="Print a list of available tests",
        action="store_true",
        dest="test_list",
        default=False,
    )
    argparser.add_argument(
        "--clean",
        help="Remove build directory in the project after running tests",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--delay-compile-errors",
        help="Compile all tests before failing on any errors",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--delay-run-errors",
        help="Compile all tests before failing on any errors",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--failed",
        help="Run the tests that failed previously (requires a .failed file in the current directory)",
        action="store_true",
        default=False
    )
    argparser.add_argument(
        "--locked",
        help="Generate locked-down workflows",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--project", help="DNAnexus project ID", default="dxCompiler_playground"
    )
    argparser.add_argument(
        "--project-wide-reuse",
        help="look for existing applets in the entire project",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--stream-all-files",
        help="Stream all input files with dxfs2",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--runtime-debug-level",
        help="printing verbosity of task/workflow runner, {0,1,2}",
    )
    argparser.add_argument(
        "--test", help="Run a test, or a subgroup of tests", action="append", default=[]
    )
    argparser.add_argument(
        "--unlocked",
        help="Generate only unlocked workflows",
        action="store_true",
        default=False,
    )
    argparser.add_argument(
        "--verbose", help="Verbose compilation", action="store_true", default=False
    )
    argparser.add_argument(
        "--verbose-key", help="Verbose compilation", action="append", default=[]
    )
    args = argparser.parse_args()

    print("top_dir={} test_dir={}".format(top_dir, test_dir))

    register_all_tests(args.verbose)
    if args.test_list:
        print_test_list()
        exit(0)
    test_names = []
    if args.failed and os.path.exists(".failed"):
        with open(".failed", "rt") as inp:
            test_names = [t.strip() for t in inp.readlines()]
    elif args.test:
        for t in args.test:
            test_names += choose_tests(t)
    elif args.build != "only":
        test_names = choose_tests("M")
    if test_names:
        print("Running tests {}".format(test_names))
    version_id = util.get_version_id(top_dir)

    project = util.get_project(args.project)
    if project is None:
        raise RuntimeError("Could not find project {}".format(args.project))
    if args.folder is None:
        base_folder = util.create_build_dirs(project, version_id)
    else:
        # Use existing prebuilt base folder
        base_folder = args.folder
        util.create_build_subdirs(project, base_folder)
    applet_folder = base_folder + "/applets"
    test_folder = base_folder + "/test"
    print("project: {} ({})".format(project.name, project.get_id()))
    print("folder: {}".format(base_folder))

    test_dict = {"aws:us-east-1": project.name + ":" + base_folder}

    # build the dxCompiler jar file, only on us-east-1
    assets = util.build(project, base_folder, version_id, top_dir, test_dict,
                        force=args.build is not None)
    print("assets: {}".format(assets))

    if args.build == "only":
        exit(0)

    if args.unlocked:
        # Disable all locked workflows
        args.locked = False
        test_unlocked = test_names

    compiler_flags = []
    if args.locked:
        compiler_flags.append("-locked")
        test_unlocked = set()
    if args.archive:
        compiler_flags.append("-archive")
    if args.compile_mode:
        compiler_flags += ["-compileMode", args.compile_mode]
    if args.force:
        compiler_flags.append("-force")
    if args.verbose:
        compiler_flags.append("-verbose")
    if args.stream_all_files:
        compiler_flags.append("-streamAllFiles")
    if args.verbose_key:
        for key in args.verbose_key:
            compiler_flags += ["-verboseKey", key]
    if args.runtime_debug_level:
        compiler_flags += ["-runtimeDebugLevel", args.runtime_debug_level]
    if args.project_wide_reuse:
        compiler_flags.append("-projectWideReuse")

    #  is "native" included in one of the test names?
    if "call_native" in test_names or "call_native_v1" in test_names:
        native_call_setup(project, applet_folder, version_id, args.verbose)
    if "call_native_app" in test_names:
        native_call_app_setup(version_id, args.verbose)

    try:
        # Compile the WDL files to dx:workflows and dx:applets
        runnable = compile_tests_to_project(
            project,
            test_names,
            applet_folder,
            compiler_flags,
            version_id,
            args.lazy,
            args.delay_compile_errors,
        )
        if not args.compile_only:
            run_test_subset(
                project,
                runnable,
                test_folder,
                args.debug,
                args.delay_workspace_destruction,
                args.delay_run_errors,
            )
    finally:
        if args.clean:
            project.remove_folder(base_folder, recurse=True, force=True)
        print("Completed running tasks in {}".format(args.project))


if __name__ == "__main__":
    main()
