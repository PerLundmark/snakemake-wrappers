__author__ = "Per Lundmark"
__copyright__ = "Copyright 2026, Per Lundmark"
__email__ = "per.lundmark@scilifelab.uu.se"
__license__ = "MIT"


import sys
from snakemake.shell import shell
from snakemake_wrapper_utils.bcftools import get_bcftools_opts
from snakemake_wrapper_utils.snakemake import is_arg

# `bcftools annotate` has no `--fasta-ref`, `--targets-file` or `--max-mem` options
bcftools_opts = get_bcftools_opts(
    snakemake, parse_ref=False, parse_targets=False, parse_memory=False
)
extra = snakemake.params.get("extra", "")
log = snakemake.log_fmt_shell(stdout=True, stderr=True)


def file_opt(input_name, flag, short_flag=None):
    """Translate an optional named input file into its bcftools option."""
    if is_arg(flag, extra) or (short_flag and is_arg(short_flag, extra)):
        flags = f"{short_flag}/{flag}" if short_flag else flag
        sys.exit(
            f"You have specified `{flags}` in `params.extra`; this is automatically "
            f"inferred from the `{input_name}` input file."
        )
    path = snakemake.input.get(input_name, "")
    return f"{flag} {path}" if path else ""


annotations = file_opt("annotations", "--annotations", "-a")
header_lines = file_opt("header_lines", "--header-lines", "-h")
rename_chrs = file_opt("rename_chrs", "--rename-chrs")
rename_annots = file_opt("rename_annots", "--rename-annots")


shell(
    "bcftools annotate"
    " {bcftools_opts}"
    " {annotations}"
    " {header_lines}"
    " {rename_chrs}"
    " {rename_annots}"
    " {extra}"
    " {snakemake.input[0]}"
    " {log}"
)
