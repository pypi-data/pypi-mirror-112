# JFP(JAR FILE PATCH)

## Usage:

help:

> jfp --help

make a patch file:

> jfp --create dest-20210709.jar --file dest-20210605.jar --output 20210709.patch

apply a patch file:

> jfp --apply 20210709.patch --output newest-20210709.jar