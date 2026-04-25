#!/usr/bin/env python3
"""
IPアドレス（CIDR表記）の一覧を比較するスクリプト
2つのファイルのIP一覧の差分を出力します
"""

import sys
from pathlib import Path
from ipaddress import ip_network, AddressValueError


def load_ip_list(file_path):
    """
    ファイルからIPアドレス（CIDR表記）の一覧を読み込む
    
    Args:
        file_path (str): ファイルパス
        
    Returns:
        set: ip_networkオブジェクトのセット
        
    Raises:
        FileNotFoundError: ファイルが見つからない場合
    """
    ip_set = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                # コメント行と空行をスキップ
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                try:
                    # IPアドレスをパース
                    network = ip_network(line, strict=False)
                    ip_set.add(network)
                except AddressValueError as e:
                    print(f"警告: {file_path} の行 {line_num} でエラー: {line}")
                    print(f"  詳細: {e}")
                    
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません: {file_path}")
        sys.exit(1)
        
    return ip_set


def compare_ip_lists(file1, file2):
    """
    2つのIPアドレス一覧を比較し、差分を出力
    
    Args:
        file1 (str): 比較元ファイル1
        file2 (str): 比較元ファイル2
    """
    p1, p2 = Path(file1), Path(file2)
    label1, label2 = p1.name, p2.name
    if label1 == label2:
        label1, label2 = p1.as_posix(), p2.as_posix()

    print(f"読み込み中: {file1}")
    ip_list1 = load_ip_list(file1)
    print(f"  読み込み件数: {len(ip_list1)}\n")
    
    print(f"読み込み中: {file2}")
    ip_list2 = load_ip_list(file2)
    print(f"  読み込み件数: {len(ip_list2)}\n")
    
    # 差分を計算
    only_in_file1 = ip_list1 - ip_list2
    only_in_file2 = ip_list2 - ip_list1
    common = ip_list1 & ip_list2
    
    # 結果を出力
    print("=" * 60)
    print("比較結果")
    print("=" * 60)
    
    print(f"\n【共通するIP】: {len(common)}件")
    if common:
        for ip in sorted(common):
            print(f"  {ip}")
    else:
        print("  なし")
    
    print(f"\n【{label1} にのみ存在】: {len(only_in_file1)}件")
    if only_in_file1:
        for ip in sorted(only_in_file1):
            print(f"  {ip}")
    else:
        print("  なし")
    
    print(f"\n【{label2} にのみ存在】: {len(only_in_file2)}件")
    if only_in_file2:
        for ip in sorted(only_in_file2):
            print(f"  {ip}")
    else:
        print("  なし")
    
    print(f"\n【統計情報】")
    print(f"  {label1} の合計: {len(ip_list1)}")
    print(f"  {label2} の合計: {len(ip_list2)}")
    print(f"  共通: {len(common)}")
    print(f"  差分: {len(only_in_file1) + len(only_in_file2)}")


def main():
    """メイン処理"""
    if len(sys.argv) != 3:
        print("使用方法: python3 src/ip_compare.py <ファイル1> <ファイル2>")
        print("\nファイル形式:")
        print("  - 1行に1つのIPアドレス（CIDR表記: xx.xx.xx.xx/xx）")
        print("  - '#' で始まる行はコメント")
        print("  - 空行は無視される")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    compare_ip_lists(file1, file2)


if __name__ == "__main__":
    main()
