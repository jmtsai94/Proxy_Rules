#!/usr/bin/env python3
import urllib.request
import re
import os
import time

# Configuration of output files and their upstream rule sources
RULE_CONFIGS = {
    "AI.list": [
        "https://raw.githubusercontent.com/666OS/rules/refs/heads/release/mihomo/AI.txt",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Gemini/Gemini.list",
        "https://ddgksf2013.top/filter/Ai.yaml",
        "https://github.com/fmz200/wool_scripts/raw/main/Loon/rule/AI.list"
    ],
    "Streaming.list": [
        "https://raw.githubusercontent.com/ddgksf2013/Filter/master/Streaming.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Netflix/Netflix.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Disney/Disney.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/TikTok/TikTok.list"
    ],
    "Proxy.list": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/QuantumultX/Proxy/Proxy.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Google/Google.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Spotify/Spotify.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/GitHub/GitHub.list",
        "https://raw.githubusercontent.com/ConnersHua/RuleGo/master/Surge/Ruleset/Proxy.list"
    ],
    "direct.list": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/WeChat/WeChat.list",
        "https://raw.githubusercontent.com/ConnersHua/RuleGo/master/Surge/Ruleset/Direct+.list",
        "https://raw.githubusercontent.com/ddgksf2013/Filter/master/Unbreak.list",
        "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/filterFix.list"
    ],
    "Crypto.list": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/QuantumultX/Crypto/Crypto.list",
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/refs/heads/master/rule/QuantumultX/Cryptocurrency/Cryptocurrency.list"
    ],
    "advertising.list": [
        "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/filter/filter.list"
    ],
    "apple.list": [
        "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/QuantumultX/Apple/Apple.list"
    ],
    "HK_Broker.list": [
        "https://raw.githubusercontent.com/LingJingMaster/Shadowrocket-Rules/main/HK_Broker.list",
        "Rules/Source/Filter_HKBroker.snippet"
    ]
}

# Configuration of rewrite files to merge
REWRITE_CONFIGS = {
    "Rewrite.snippet": [
        "https://github.com/fmz200/wool_scripts/raw/main/QuantumultX/rewrite/split/part!!/AffiliateMarketing.snippet",
        "Rules/Source/REWRITE_LOFTER.snippet",
        "https://github.com/fmz200/wool_scripts/raw/main/QuantumultX/rewrite/split/partX/XueQiu.snippet",
        "https://raw.githubusercontent.com/ddgksf2013/Rewrite/refs/heads/master/AdBlock/Applet.conf",
        "https://github.com/fmz200/wool_scripts/raw/main/QuantumultX/rewrite/split/partY/YouTube.snippet",
        "https://github.com/fmz200/wool_scripts/raw/main/QuantumultX/rewrite/split/partX/Xiaohongshu.snippet",
        "https://raw.githubusercontent.com/fmz200/wool_scripts/main/QuantumultX/rewrite/weibo.snippet",
        "https://ddgksf2013.top/rewrite/BiliBiliAdsLite.conf",
        "https://raw.githubusercontent.com/Sliverkiss/QuantumultX/refs/heads/main/Script/switchMode.js",
        "https://raw.githubusercontent.com/NobyDa/Script/master/QuantumultX/Snippet/GoogleCAPTCHA.snippet",
        "https://raw.githubusercontent.com/wf021325/qx/master/js/jd_price.js",
        "https://github.com/ddgksf2013/Rewrite/raw/master/Html/General.conf",
        "https://raw.githubusercontent.com/ddgksf2013/Rewrite/master/Function/UnblockURLinWeChat.conf"
    ]
}

def fetch_content(url, retries=3):
    for i in range(retries):
        print(f"Fetching (Attempt {i+1}/{retries}): {url}")
        # Use Quantumult X User-Agent to bypass browser checking on some rule/rewrite hosting sites (e.g. ddgksf2013.top)
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Quantumult X/1.4.3'}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"Error fetching {url} on attempt {i+1}: {e}")
            if i == retries - 1:
                return ""
            time.sleep(2)

def read_local_file(filepath):
    print(f"Reading local file: {filepath}")
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading local file {filepath}: {e}")
    else:
        print(f"Local file not found: {filepath}")
    return ""

def parse_rules(content):
    rules = set()
    # Regex to match rule types and values
    pattern = re.compile(
        r'\b(DOMAIN|DOMAIN-SUFFIX|DOMAIN-KEYWORD|HOST|HOST-SUFFIX|HOST-KEYWORD|IP-CIDR|IP-CIDR6|IP6-CIDR|USER-AGENT),\s*([a-zA-Z0-9_\-\.\:\/*?]+)',
        re.IGNORECASE
    )
    
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith(('#', '//', ';', '!')):
            continue
            
        for comment_char in ('#', ';', '//'):
            if comment_char in line:
                line = line.split(comment_char)[0].strip()
                
        if line.startswith('- '):
            line = line[2:].strip()
            
        matches = pattern.findall(line)
        for rule_type, rule_val in matches:
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
                
            if rule_type in ('HOST', 'HOST-SUFFIX'):
                rule_val = rule_val.lower()
                
            rules.add((rule_type, rule_val))
            
    return rules

def parse_rewrite(content, is_js=False):
    filter_rules = []
    rewrite_rules = []
    hostnames = set()
    
    # If JS file, extract content from block comments /* ... */
    if is_js:
        blocks = re.findall(r'/\*(.*?)\*/', content, re.DOTALL)
        content = "\n".join(blocks)
        
    filter_types = {'DOMAIN', 'DOMAIN-SUFFIX', 'DOMAIN-KEYWORD', 'HOST', 'HOST-SUFFIX', 'HOST-KEYWORD', 'IP-CIDR', 'IP-CIDR6', 'IP6-CIDR', 'USER-AGENT', 'GEOIP'}
        
    for line in content.splitlines():
        line = line.strip()
        # Skip empty lines, pure comment lines, user script tags
        if not line or line.startswith(('#', ';', '//', '/*', '*/', '==UserScript==', '@', '==/UserScript==')):
            continue
            
        # Parse hostname line
        if line.lower().startswith('hostname'):
            parts = line.split('=', 1)
            if len(parts) == 2:
                hosts_str = parts[1].strip()
                # Remove %APPEND% or %ADD% prefixes
                hosts_str = re.sub(r'%(APPEND|ADD)%', '', hosts_str, flags=re.IGNORECASE).strip()
                for h in hosts_str.split(','):
                    h = h.strip()
                    if h:
                        hostnames.add(h)
            continue
            
        # Skip section headers
        if line.lower() in ('[rewrite_local]', '[mitm]', '[rewrite_remote]', '[task_local]', '[script]', '[filter_local]'):
            continue
            
        # Check if it's a filter rule
        parts = line.split(',', 1)
        first_part = parts[0].strip().upper()
        if first_part in filter_types:
            rule_type = first_part
            if rule_type == 'DOMAIN':
                rule_type = 'HOST'
            elif rule_type == 'DOMAIN-SUFFIX':
                rule_type = 'HOST-SUFFIX'
            elif rule_type == 'DOMAIN-KEYWORD':
                rule_type = 'HOST-KEYWORD'
            elif rule_type == 'IP-CIDR6':
                rule_type = 'IP6-CIDR'
                
            rule_val = parts[1].strip()
            # Lowercase domains in HOST and HOST-SUFFIX for consistency
            if rule_type in ('HOST', 'HOST-SUFFIX'):
                subparts = rule_val.split(',', 1)
                subparts[0] = subparts[0].lower()
                rule_val = ",".join(subparts)
                
            filter_rules.append(f"{rule_type},{rule_val}")
            continue
            
        # Check if it's a rewrite rule using strict action checks to filter out JS code lines
        if re.search(r'\s+url\s+(reject|reject-200|reject-img|reject-dict|reject-array|302|307|response-body|request-body|request-header|response-header|script-[\w\-]+)', line, re.IGNORECASE):
            rewrite_rules.append(line)
        
    return filter_rules, rewrite_rules, hostnames

def main():
    output_dir = "Rules"
    os.makedirs(output_dir, exist_ok=True)
    
    # Remove old AI.list from root if it exists
    old_ai_list = "AI.list"
    if os.path.exists(old_ai_list):
        try:
            os.remove(old_ai_list)
            print(f"Removed old {old_ai_list} from root directory.")
        except Exception as e:
            print(f"Error removing old {old_ai_list}: {e}")
            
    # 1. Process rule lists
    for filename, urls in RULE_CONFIGS.items():
        print(f"\n=== Processing Rule List: {filename} ===")
        all_rules = set()
        for url_or_path in urls:
            if url_or_path.startswith(('http://', 'https://')):
                content = fetch_content(url_or_path)
            else:
                content = read_local_file(url_or_path)
                
            if content:
                rules = parse_rules(content)
                print(f"Parsed {len(rules)} unique rules from {url_or_path}")
                all_rules.update(rules)
                
        print(f"Total unique rules merged for {filename}: {len(all_rules)}")
        
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
        
        output_file = os.path.join(output_dir, filename)
        policy_placeholder = filename.split('.')[0]
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# NAME: {filename.split('.')[0]} Rules\n")
                f.write(f"# TOTAL: {len(sorted_rules)}\n")
                f.write("# UPDATED: Auto-updated\n\n")
                for r_type, r_val in sorted_rules:
                    f.write(f"{r_type},{r_val},{policy_placeholder}\n")
            print(f"Successfully wrote {len(sorted_rules)} rules to {output_file}")
        except Exception as e:
            print(f"Error writing {output_file}: {e}")

    # 2. Process rewrites
    for filename, urls in REWRITE_CONFIGS.items():
        print(f"\n=== Processing Rewrite File: {filename} ===")
        all_filters_ordered = []
        seen_filters = set()
        all_rewrites_ordered = []
        seen_rewrites = set()
        all_hostnames = set()
        
        for url_or_path in urls:
            if url_or_path.startswith(('http://', 'https://')):
                content = fetch_content(url_or_path)
            else:
                content = read_local_file(url_or_path)
                
            if content:
                is_js = url_or_path.endswith('.js')
                filters, rewrites, hostnames = parse_rewrite(content, is_js=is_js)
                print(f"Parsed {len(filters)} filters, {len(rewrites)} rewrites, and {len(hostnames)} hostnames from {url_or_path}")
                
                # Merge filters preserving order
                for f_rule in filters:
                    if f_rule not in seen_filters:
                        seen_filters.add(f_rule)
                        all_filters_ordered.append(f_rule)
                        
                # Merge rewrites preserving order
                for r in rewrites:
                    if r not in seen_rewrites:
                        seen_rewrites.add(r)
                        all_rewrites_ordered.append(r)
                
                # Merge hostnames
                all_hostnames.update(hostnames)
                
        print(f"Total merged filters: {len(all_filters_ordered)}, rewrites: {len(all_rewrites_ordered)}, hostnames: {len(all_hostnames)}")
        
        output_file = os.path.join(output_dir, filename)
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# NAME: Merged Rewrite Rules ({filename.split('.')[0]})\n")
                f.write(f"# TOTAL FILTERS: {len(all_filters_ordered)}\n")
                f.write(f"# TOTAL REWRITES: {len(all_rewrites_ordered)}\n")
                f.write(f"# TOTAL HOSTNAMES: {len(all_hostnames)}\n")
                f.write("# UPDATED: Auto-updated\n\n")
                
                # Output all rules directly without headers to comply with remote rewrite parser
                if all_filters_ordered:
                    f.write("# === Filter Rules ===\n")
                    for filter_rule in all_filters_ordered:
                        f.write(f"{filter_rule}\n")
                    f.write("\n")
                
                if all_rewrites_ordered:
                    f.write("# === Rewrite Rules ===\n")
                    for rule in all_rewrites_ordered:
                        f.write(f"{rule}\n")
                    f.write("\n")
                    
                if all_hostnames:
                    f.write("# === MitM Hostnames ===\n")
                    hostname_str = ", ".join(sorted(all_hostnames))
                    f.write(f"hostname = {hostname_str}\n")
                
            print(f"Successfully wrote rewrite rules to {output_file}")
        except Exception as e:
            print(f"Error writing {output_file}: {e}")

if __name__ == "__main__":
    main()
