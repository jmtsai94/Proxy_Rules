#!/usr/bin/env python3
import urllib.request
import re
import os

# URLs to fetch rules from
URLS = [
    "https://raw.githubusercontent.com/666OS/rules/refs/heads/release/mihomo/AI.txt",
    "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Gemini/Gemini.list",
    "https://ddgksf2013.top/filter/Ai.yaml",
    "https://github.com/fmz200/wool_scripts/raw/main/Loon/rule/AI.list"
]

def fetch_content(url):
    print(f"Fetching: {url}")
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

def parse_rules(content):
    rules = set()
    # Regex to match rule types and values:
    # Matches: TYPE,VALUE where TYPE is DOMAIN, DOMAIN-SUFFIX, DOMAIN-KEYWORD, HOST, HOST-SUFFIX, HOST-KEYWORD, IP-CIDR, IP-CIDR6, IP6-CIDR, USER-AGENT
    # and VALUE is domain, IP/CIDR, keyword, or user-agent pattern.
    pattern = re.compile(
        r'\b(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|HOST|HOST-SUFFIX|HOST-KEYWORD|IP-CIDR|IP-CIDR6|IP6-CIDR|USER-AGENT),\s*([a-zA-Z0-9_\-\.\:\/*?]+)',
        re.IGNORECASE
    )
    
    for line in content.splitlines():
        line = line.strip()
        # Skip empty lines or full line comments
        if not line or line.startswith(('#', '//', ';', '!')):
            continue
            
        # Strip trailing comments
        for comment_char in ('#', ';', '//'):
            if comment_char in line:
                # Make sure the comment char is not part of a value (e.g., inside a regex or URL if any, but rule values don't have these)
                line = line.split(comment_char)[0].strip()
                
        # Handle YAML format list item prefix "- "
        if line.startswith('- '):
            line = line[2:].strip()
            
        # Find all matching rule pairs in the line (handles Loon's AND/OR rules since we extract components)
        matches = pattern.findall(line)
        for rule_type, rule_val in matches:
            # Map type to QX equivalent
            rule_type = rule_type.upper()
            if rule_type == 'DOMAIN':
                rule_type = 'HOST'
            elif rule_type == 'DOMAIN-SUFFIX':
                rule_type = 'HOST-SUFFIX'
            elif rule_type == 'DOMAIN-KEYWORD':
                rule_type = 'HOST-KEYWORD'
            elif rule_type == 'IP-CIDR6':
                rule_type = 'IP6-CIDR'
            elif rule_type == 'IP6-CIDR':
                rule_type = 'IP6-CIDR'
            elif rule_type == 'USER-AGENT':
                rule_type = 'USER-AGENT'
                
            # Domain names in HOST and HOST-SUFFIX are case-insensitive, so lowercase them.
            if rule_type in ('HOST', 'HOST-SUFFIX'):
                rule_val = rule_val.lower()
                
            rules.add((rule_type, rule_val))
            
    return rules

def main():
    all_rules = set()
    for url in URLS:
        content = fetch_content(url)
        if content:
            rules = parse_rules(content)
            print(f"Parsed {len(rules)} unique rules from {url}")
            all_rules.update(rules)
            
    print(f"Total unique rules merged: {len(all_rules)}")
    
    # Sort rules: Group by type, then sort alphabetically by value
    type_priority = {
        'HOST': 1,
        'HOST-SUFFIX': 2,
        'HOST-KEYWORD': 3,
        'IP-CIDR': 4,
        'IP6-CIDR': 5,
        'USER-AGENT': 6
    }
    
    sorted_rules = sorted(
        all_rules,
        key=lambda r: (type_priority.get(r[0], 99), r[1])
    )
    
    output_file = "AI.list"
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# NAME: AI Rules\n")
            f.write(f"# TOTAL: {len(sorted_rules)}\n")
            f.write("# UPDATED: Auto-updated\n\n")
            for r_type, r_val in sorted_rules:
                f.write(f"{r_type},{r_val}\n")
        print(f"Successfully wrote {len(sorted_rules)} rules to {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
