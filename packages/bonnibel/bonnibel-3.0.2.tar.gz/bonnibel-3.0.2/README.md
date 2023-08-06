# Bonnibel

Bonnibel (`pb` for short) builds [Ninja][] build files for a set of modules.
Bonnibel doesn't try to hide Ninja's build files or syntax from the user. It
mostly exists to do the legwork of auto-generating all the build rules, while
letting the user control the variables used or even write custom rules.
Bonnibel's configs let you define a _project_, and a set of _modules_ within
that project to be built. You must also specify a _configuration_ file to set
the base compilation programs and arguments for earch _target_ platform.

For example, Bonnibel was created for [jsix][], where I needed the ability to
build tools or libraries for my multiple target environments (e.g., for use
both in the UEFI bootloader and in the kernel), while building the bootloader,
kernel and user-space applications all with different compiler and linker
options. See jsix's build files for an example of use.

[Ninja]: https://ninja-build.org
[jsix]: https://github.com/justinian/jsix
