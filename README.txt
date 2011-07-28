Developing...

Required software:
    * Ant 1.8.0 or higher.
    * Python 2.7.x.

Setup:
    1. Locate this directory that names "build" at top directory of application
       project.
    2. Copy or make symbolic link from build-start-scripts/start-build.py.
    3. Copy the below and paste to the below of <setup /> at build.xml.

            <if condition="${extended.build}">
                <then>
                    <import file="build/extended_build.xml" />
                </then>
            </if>


FindBugs Setup:
    1. Install FindBugs to externals/findbugs or other directory.
    2. Locate findbugs-ant.jar to externals/lib or library directory of Ant.
    3. Turn true findbugs.enable in config/extension.properties.
    4. Modify findbugs.home to directory installed FindBugs if you need.
