from icecream import ic 
from pprint import pprint
import sys
import re

def count_imbalances(line: str) -> int:
    """
    Count number of starting braces without ending braces
    """
    count = 0
    for char in line:
        if char == "{":
            count += 1
        elif char == "}":
            count -= 1
    return count


def fix_line_imbalances(lines: list[str]) -> list[str]:
    """
    If line contains starting brace without ending brace, need to combine lines until ending brace match found
    """

    new_lines = []

    i = 0
    while i < len(lines):
        line = lines[i]
        while count_imbalances(line) != 0:
            # keep adding lines until ending brace match found
            i += 1
            line += " " + lines[i]

            if i >= len(lines):
                raise Exception("Line imbalance not closed at end of lines. Got to: " + line)
        # line is balanced, add it to new lines

        new_lines.append(line)
        i+=1

    return new_lines

def handle_nref(lines: list[str]) -> tuple[list[str], dict[str,str]]:
    """
    The \\nref command defines a bibliography entry without immediately citing it.
    Stores this entry into a bibliography dictionary.
    Removes the command from the lines.

    So a line like
    \\nref\\om{Montonen and Olive, Phys. Lett. B72 (1977) 117;}
    would add the entry
    "om": "Montonen and Olive, Phys. Lett. B72 (1977) 117;"
    and remove the command "\\om" from all lines, converting its usage to "\\cite{om}"
    """

    import re
    
    bibliography = {}
    new_lines = []
    ref_keys = set()  # Track all reference keys found

    # First pass: extract all \nref definitions and build bibliography
    for line in lines:
        # Find all \nref\KEY{ patterns and extract content with proper brace handling
        nref_start_pattern = r'\\nref\\(\w+)\{'
        result_line = line
        offset = 0
        
        for match in re.finditer(nref_start_pattern, line):
            key = match.group(1)
            start_pos = match.end()
            
            # Find matching closing brace, accounting for nested braces
            brace_count = 1
            end_pos = start_pos
            while end_pos < len(line) and brace_count > 0:
                if line[end_pos] == '{':
                    brace_count += 1
                elif line[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1
            
            if brace_count == 0:
                # Successfully found matching brace
                content = line[start_pos:end_pos-1]
                bibliography[key] = content
                ref_keys.add(key)
                
                # Remove the \nref\KEY{...} from the result
                nref_end = match.start()
                result_line = result_line[:nref_end-offset] + result_line[end_pos-offset:]
                offset += end_pos - nref_end
        
        new_lines.append(result_line)
    
    # Second pass: replace all \KEY\ usages with \cite{KEY}
    final_lines = []
    for line in new_lines:
        for key in ref_keys:
            # Pattern: \KEY\ (backslash followed by key name and backslash)
            line = line.replace(f"\\{key}\\", f"\\cite{{{key}}}")
        final_lines.append(line)

    return (final_lines, bibliography)

def handle_ref(lines: list[str]) -> tuple[list[str], dict[str,str]]:
    """
    The \\ref command defines a bibliography entry and cites it.
    Store this entry into a bibliography dictionary to be returned.
    Convert this command to a citation command.
    
    So a line like
    \\ref\\wo{E. Witten and D. Olive, Phys. Lett. {\\bf 78B} (1978) 97.}
    would add the entry
    "wo": "E. Witten and D. Olive, Phys. Lett. {\\bf 78B} (1978) 97."
    and replace the command with "\\cite{wo}"
    """
    import re
    
    bibliography = {}
    new_lines = []

    # Process all \ref definitions and convert them to \cite commands
    for line in lines:
        # Find all \ref\KEY{ patterns and extract content with proper brace handling
        ref_start_pattern = r'\\ref\\(\w+)\{'
        result_line = line
        offset = 0
        
        for match in re.finditer(ref_start_pattern, line):
            key = match.group(1)
            start_pos = match.end()
            
            # Find matching closing brace, accounting for nested braces
            brace_count = 1
            end_pos = start_pos
            while end_pos < len(line) and brace_count > 0:
                if line[end_pos] == '{':
                    brace_count += 1
                elif line[end_pos] == '}':
                    brace_count -= 1
                end_pos += 1
            
            if brace_count == 0:
                # Successfully found matching brace
                content = line[start_pos:end_pos-1]
                bibliography[key] = content
                
                # Replace the \ref\KEY{...} with \cite{KEY}
                ref_start = match.start()
                replacement = f"\\cite{{{key}}}"
                result_line = result_line[:ref_start-offset] + replacement + result_line[end_pos-offset:]
                offset += end_pos - ref_start - len(replacement)
        
        new_lines.append(result_line)

    return (new_lines, bibliography)

def convert_reference_instances(lines: list[str], ref_names: list[str]) -> list[str]:
    """
    Given a list of reference names, replace all instances of \\ref\\NAME with \\cite{NAME}
    """

    new_lines = []

    for i, line in enumerate(lines):
        for ref in ref_names:
            new_line = re.sub(rf"\\{ref}\b", rf"\\cite{{{ref}}}", line)
            if new_line != line:
                line = new_line
        new_lines.append(line)

    return new_lines

def convert_section_commands(lines: list[str]) -> list[str]:
    """
    \\subsec{} -> \\subsection{}
    \\newsec{} -> \\section{}
    """

    new_lines = []

    for line in lines:
        if re.match(r"\\subsec\{(.*)\}", line):
            new_line = r"\subsection{" + re.sub(r"\\subsec\{(.*)\}", r"\1", line) + r"}"
            new_lines.append(new_line)
        elif re.match(r"\\newsec\{(.*)\}", line):
            new_line = r"\section{" + re.sub(r"\\newsec\{(.*)\}", r"\1", line) + r"}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    return new_lines

def write_unordered_bib(bibliography: dict[str,str], filename="unordered_bib.tex"):
    """
    Writes the bibliography to a file
    """
    with open(filename, "w") as f:
        for key, content in bibliography.items():
            f.write(f"\\bibitem{{{key}}}\n")
            f.write(content)
            f.write("\n")

def construct_ordered_bib(lines: list[str], bibliography: dict[str,str]) -> dict[str,str]:
    ordered_bib = {}
    bib_keys = list(bibliography.keys())

    def add_to_ordered_bib(key:str):
        if key in ordered_bib:
            return
        ordered_bib[key] = bibliography[key]

    for line in lines:
        m = re.search(r"\\cite\{(.*?)\}", line)
        if m:
            # print("cite matches:", m, "line:", line, "key:", m.group(1))
        
            ref_arg = m.group(1)
            if ',' in ref_arg: 
                # Multiple keys
                cite_keys = ref_arg.split(',')
                for cite_key in cite_keys:
                    cite_key = cite_key.strip()
                    add_to_ordered_bib(cite_key)
            elif '-' in ref_arg:
                # range
                keys = ref_arg.split('-')
                assert len(keys) == 2, f"range of keys format unexpected: {keys}"
                start_key = keys[0].strip()
                end_key = keys[1].strip()
                start_key_idx = bib_keys.index(start_key)
                end_key_idx = bib_keys.index(end_key)
                assert start_key_idx >= 0 and end_key_idx >= 0, f"range of keys {start_key}-{end_key} is empty"
                assert start_key_idx <= end_key_idx, f"range of keys {start_key}-{end_key} is empty"

                for i in range(start_key_idx, end_key_idx+1):
                    add_to_ordered_bib(bib_keys[i])

            else:
                # Single key
                cite_key = ref_arg.strip()
                add_to_ordered_bib(cite_key)
    

    if len(ordered_bib) != len(bibliography):
        print("missing keys: ", list(set(bibliography.keys()) - set(ordered_bib.keys())))
    return ordered_bib


def write_output(lines: list[str], bibliography: dict[str,str], filename: str):
    """
    Writes the output to a file
    """
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
            f.write("\n")
        

        f.write("\n\n")
        f.write("\\begin{thebibliography}{99}\n")

        for key, content in construct_ordered_bib(lines, bibliography).items():
            f.write(f"\\bibitem{{{key}}}\n")
            f.write(content)
            f.write("\n")
        f.write("\\end{thebibliography}\n")

def convert_refs_command(lines: list[str], bib: dict[str,str]) -> list[str]:
    """
    \\refs{\\refname1,\\refname2} becomes \\cite{refname1,refname2}

    \\refs{ \\refnameA - \\refnameD } is citing a range of keys
    Should expand it into \\cite{refnameA,refnameB,refnameC,refnameD}
    
    """
    import re
    
    new_lines = []
    bib_keys = list(bib.keys())
    
    for line in lines:
        # search for \refs{...} pattern in the line
        refs_pattern = r'\\refs\{(.*?)\}'
        # m = re.search(refs_pattern, line)
        # if m:
        #     print('convert_refs_command: line:', line, 'm:', m)
        #     ref_arg = m.group(1)
        #     if ',' in ref_arg:
        #         # Multiple keys
        #         cite_keys = ref_arg.split(',')
        
        def convert_refs_arg(match):
            """Convert the argument of \\refs{...} command to \\cite{...} command"""

            content = match.group(1)
            keys = []
            if ',' in content: # multiple keys
                for key in content.split(','):
                    key = key.strip().replace('\\', '')
                    keys.append(key)
            elif '-' in content: # range of keys
                startkey, endkey = content.split('-')
                startkey = startkey.strip().replace('\\', '')
                endkey = endkey.strip().replace('\\', '')
                start_index = bib_keys.index(startkey)
                end_index = bib_keys.index(endkey)
                for i in range(start_index, end_index+1):
                    keys.append(bib_keys[i])
            else:
                raise Exception("Unexpected format of \\refs{...} argument: " + content)


            new_content = ",".join(keys)

            return f"\\cite{{{new_content}}}"
        
        new_line = re.sub(refs_pattern, convert_refs_arg, line)

        new_lines.append(new_line)

    return new_lines

def find_matching_brace(text: str, start_pos: int) -> int:
    """
    Given a position of an opening brace, find the matching closing brace.
    Handles nested braces correctly.
    Returns the position of the closing brace, or -1 if not found.
    """
    if start_pos >= len(text) or text[start_pos] != '{':
        return -1
    
    brace_count = 1
    pos = start_pos + 1
    while pos < len(text) and brace_count > 0:
        if text[pos] == '{':
            brace_count += 1
        elif text[pos] == '}':
            brace_count -= 1
        pos += 1
    
    if brace_count == 0:
        return pos - 1  # Return position of closing brace
    return -1

def convert_pmatrix(line: str) -> str:
    """
    Convert \\pmatrix{...} -> \\begin{pmatrix}...\\end{pmatrix}
    Handles nested braces correctly.
    """
    result = ""
    pos = 0
    
    while pos < len(line):
        idx = line.find("\\pmatrix{", pos)
        if idx == -1:
            result += line[pos:]
            break
        
        result += line[pos:idx]
        brace_start = idx + len("\\pmatrix")
        brace_end = find_matching_brace(line, brace_start)
        
        if brace_end == -1:
            result += line[idx:brace_start + 1]
            pos = brace_start + 1
        else:
            content = line[brace_start + 1:brace_end]
            result += f"\\begin{{pmatrix}}{content}\\end{{pmatrix}}"
            pos = brace_end + 1
    
    return result

def convert_eqalign(line: str) -> str:
    """
    Convert \\eqalign{...} -> \\begin{aligned}...\\end{aligned}
    Handles nested braces correctly.
    """
    result = ""
    pos = 0
    
    while pos < len(line):
        idx = line.find("\\eqalign{", pos)
        if idx == -1:
            result += line[pos:]
            break
        
        result += line[pos:idx]
        brace_start = idx + len("\\eqalign")
        brace_end = find_matching_brace(line, brace_start)
        
        if brace_end == -1:
            result += line[idx:brace_start + 1]
            pos = brace_start + 1
        else:
            content = line[brace_start + 1:brace_end]
            result += f"\\begin{{aligned}}{content}\\end{{aligned}}"
            pos = brace_end + 1
    
    return result

def convert_over(line: str) -> str:
    """
    Convert {... \\over ...} -> \\frac{...}{...}
    Handles nested braces correctly by parsing from innermost braces outward.
    """
    result = ""
    pos = 0
    
    while pos < len(line):
        # Find opening brace
        idx = line.find("{", pos)
        if idx == -1:
            result += line[pos:]
            break
        
        result += line[pos:idx]
        brace_end = find_matching_brace(line, idx)
        
        if brace_end == -1:
            result += line[idx]
            pos = idx + 1
            continue
        
        content = line[idx + 1:brace_end]
        
        # Check if this content contains \over
        if "\\over" in content:
            over_idx = content.find("\\over")
            numerator = content[:over_idx].strip()
            denominator = content[over_idx + len("\\over"):].strip()
            result += f"\\frac{{{numerator}}}{{{denominator}}}"
        else:
            result += "{" + content + "}"
        
        pos = brace_end + 1
    
    return result

def convert_old_tex_math_constructs(line: str) -> str:
    """
    Convert old TeX math constructs to new LaTeX math constructs.

    \\cr -> \\\\ 
    \\pmatrix{...} -> \\begin{pmatrix}...\\end{pmatrix}
    \\eqalign{...} -> \\begin{aligned}...\\end{aligned}
    {... \\over ...} -> \\frac{...}{...}

    Uses proper brace-aware parsing to handle nested braces.
    """
    new_line = line.replace("\\cr", "\\\\")
    new_line = convert_pmatrix(new_line)
    new_line = convert_eqalign(new_line)
    # new_line = convert_over(new_line)
    
    return new_line

def convert_eqn_macro(lines: list[str]) -> list[str]:
    """
    Convert occurrences of \\eqn\\eqnname{body} into a multi-line equation block:

    \\begin{equation}
    \\label{eqnname}
    body
    \\end{equation}

    If \\eqnname occurs in the rest of the text, it is converted to \\eqref{eqnname}

    Can handle multiple macros per line and nested braces inside the body.
    """
    new_lines: list[str] = []
    # collect defined equation labels so we can replace later usages
    eq_keys: list[str] = []

    for i, line in enumerate(lines):
        result = ""
        pos = 0
        while True:
            idx = line.find("\\eqn", pos)
            if idx == -1:
                result += line[pos:]
                break

            # append text before macro
            result += line[pos:idx]

            # position just after "\\eqn"
            key_start = idx + len("\\eqn")
            # skip an optional backslash before the key (i.e. \eqn\key{...})
            if key_start < len(line) and line[key_start] == "\\":
                key_start += 1

            brace_open = line.find("{", key_start)
            if brace_open == -1:
                # malformed, treat literally and advance past the found token
                result += line[idx: key_start]
                pos = key_start
                continue

            key = line[key_start:brace_open]

            # find matching closing brace, account for nested braces
            start_pos = brace_open + 1
            brace_count = 1
            end_pos = start_pos
            while end_pos < len(line) and brace_count > 0:
                if line[end_pos] == "{":
                    brace_count += 1
                elif line[end_pos] == "}":
                    brace_count -= 1
                end_pos += 1

            if brace_count != 0:
                raise Exception("Unclosed brace in \\eqn macro: " + line)

            content = line[start_pos:end_pos - 1]

            new_math = convert_old_tex_math_constructs(content)
            if new_math != content:
                content = new_math

            replacement = (
                "\\begin{equation}\n"
                f"\\label{{{key}}}\n"
                f"{content}\n"
                "\\end{equation}"
            )

            # record key for later replacement of uses like \key -> \eqref{key}
            eq_keys.append(key)

            result += replacement
            pos = end_pos

        # split any embedded newlines into separate lines
        new_lines.extend(result.split("\n"))

    # Now replace occurrences of \key with \eqref{key} 

    final_lines: list[str] = []

    for line in new_lines:
        for eq_key in eq_keys:
            new_line = re.sub(rf"\\{eq_key}\b", rf"\\eqref{{{eq_key}}}", line)
            line = new_line
        final_lines.append(line)

    return final_lines


if __name__ == "__main__":

    # Read input filename from command line if provided, otherwise default to "part.tex"
    if len(sys.argv) > 1:
        input_filename = sys.argv[1]
    else:
        input_filename = "body.tex"

    with open(input_filename, "r") as file:
        lines = file.readlines()

    # strip everything
    lines = [line.strip() for line in lines]

    # fix line imbalances, for all other parsing of lines
    lines = fix_line_imbalances(lines)

    bibliography = {}

    # convert \nref commands
    lines, new_bib_entries = handle_nref(lines)
    for key, content in new_bib_entries.items():
        bibliography[key] = content

    # convert \ref commands
    lines, new_bib_entries = handle_ref(lines)
    for key, content in new_bib_entries.items():
        bibliography[key] = content
    

    lines = convert_refs_command(lines, bibliography)
    lines = convert_reference_instances(lines, list(bibliography.keys()))

    lines = convert_section_commands(lines)

    lines = convert_eqn_macro(lines)


    # one-off conversions

    # convert \foot{...} to \footnote{...}
    lines = [re.sub(r"\\foot\{", r"\\footnote{", line) for line in lines]

    # there's a \semi in the bibliography, which is not a valid latex command
    for key, content in bibliography.items():
        if "\\semi" in content:
            bibliography[key ] = content.replace("\\semi", ";\\\\")


    write_unordered_bib(bibliography)

    # write the output to a file
    write_output(lines, bibliography, "converted.tex")

