from crewai.tools import tool
import os

@tool("Code Security Scanner")
def code_security_scanner(code: str) -> str:
    """
    Analyzes code for security vulnerabilities including SQL injection,
    XSS, command injection, and other common attack vectors.
    
    Args:
        code: The Python code to analyze for security issues.
        
    Returns:
        A security analysis report with identified vulnerabilities.
    """
    
    vulnerabilities = []
    
    if "eval(" in code or "exec(" in code:
        vulnerabilities.append("CRITICAL: Use of eval() or exec() detected - arbitrary code execution risk")
    
    if "os.system(" in code or "subprocess.call(" in code:
        vulnerabilities.append("HIGH: Direct system command execution detected - command injection risk")
    
    if "pickle.loads(" in code:
        vulnerabilities.append("HIGH: Insecure deserialization with pickle - code execution risk")
    
    if "SELECT" in code and "%" in code:
        vulnerabilities.append("HIGH: Potential SQL injection - string formatting in SQL query")
    
    if "<script>" in code.lower():
        vulnerabilities.append("MEDIUM: Potential XSS vulnerability - unescaped script tags")
    
    if not vulnerabilities:
        return "✅ Security Analysis: No obvious vulnerabilities detected. Code appears secure."
    
    report = "🔒 Security Analysis Report:\n\n"
    report += f"Found {len(vulnerabilities)} potential security issue(s):\n\n"
    for i, vuln in enumerate(vulnerabilities, 1):
        report += f"{i}. {vuln}\n"
    
    return report


@tool("Style Checker")
def style_checker(code: str) -> str:
    """
    Checks code for PEP8 compliance, formatting issues, and Python best practices.
    
    Args:
        code: The Python code to analyze for style issues.
        
    Returns:
        A style analysis report with identified issues and suggestions.
    """
    
    issues = []
    
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 79 and not line.strip().startswith('#'):
            issues.append(f"Line {i}: Exceeds 79 characters (PEP8)")
        
        if '\t' in line:
            issues.append(f"Line {i}: Uses tabs instead of spaces (PEP8)")
        
        if line.strip().endswith(';'):
            issues.append(f"Line {i}: Unnecessary semicolon (non-Pythonic)")
    
    if 'import *' in code:
        issues.append("Wildcard imports detected - violates PEP8, reduces code clarity")
    
    if code.count('\n\n\n') > 0:
        issues.append("Multiple consecutive blank lines detected - PEP8 recommends max 2")
    
    function_defs = [line for line in lines if line.strip().startswith('def ')]
    for func_line in function_defs:
        if '(' in func_line and ')' in func_line:
            func_name = func_line.split('def ')[1].split('(')[0].strip()
            if func_name and func_name[0].isupper():
                issues.append(f"Function '{func_name}' uses PascalCase - should use snake_case (PEP8)")
    
    if not issues:
        return "✅ Style Analysis: Code follows PEP8 guidelines. Well formatted!"
    
    report = "📝 Style Analysis Report:\n\n"
    report += f"Found {len(issues)} style issue(s):\n\n"
    for i, issue in enumerate(issues, 1):
        report += f"{i}. {issue}\n"
    
    return report


@tool("Complexity Analyzer")
def complexity_analyzer(code: str) -> str:
    """
    Analyzes time and space complexity, identifies performance bottlenecks,
    and suggests optimizations.
    
    Args:
        code: The Python code to analyze for performance characteristics.
        
    Returns:
        A performance analysis report with complexity and optimization suggestions.
    """
    
    findings = []
    
    nested_loops = code.count('for ') + code.count('while ')
    if nested_loops >= 3:
        findings.append(f"⚠️ Detected {nested_loops} loops - potential O(n²) or higher complexity")
    
    if 'for ' in code and 'for ' in code[code.find('for ')+4:]:
        findings.append("Nested loops detected - consider optimization (list comprehension, vectorization)")
    
    if '.append(' in code and 'for ' in code:
        findings.append("List append in loop - consider list comprehension for better performance")
    
    if 'list(' in code and 'range(' in code:
        findings.append("list(range()) detected - consider using range() directly or numpy arrays")
    
    if code.count('if ') > 5:
        findings.append("Multiple conditional branches - consider using dictionary dispatch or strategy pattern")
    
    if 'recursion' in code.lower() or code.count('def ') > 1:
        if any(func_name in code for func_name in ['fibonacci', 'factorial']):
            findings.append("Recursive function detected - consider memoization or iterative approach")
    
    if '**' in code or 'pow(' in code:
        findings.append("Exponentiation detected - verify if logarithmic alternatives are possible")
    
    if not findings:
        return "✅ Performance Analysis: Code appears efficient. No obvious bottlenecks detected."
    
    report = "⚡ Performance Analysis Report:\n\n"
    report += f"Identified {len(findings)} performance consideration(s):\n\n"
    for i, finding in enumerate(findings, 1):
        report += f"{i}. {finding}\n"
    
    report += "\n💡 General Recommendations:\n"
    report += "- Profile code with cProfile for accurate bottleneck identification\n"
    report += "- Consider algorithmic improvements before micro-optimizations\n"
    report += "- Use appropriate data structures (sets for lookups, deques for queues)\n"
    
    return report
