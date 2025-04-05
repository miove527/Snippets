import pandas as pd
import random

def read_gro(file_path, test=False, random_test_num=10):
    """
    Parses a .gro file to extract molecular dynamics simulation data.

    Parameters:
    - file_path (str): The path to the .gro file to be parsed.
    - test (bool): If True, the function will call `test_gro` to validate the parsed data.
    - random_test_num (int): The number of random lines to validate if `test` is True.

    Returns:
    - df (pd.DataFrame): A DataFrame containing the parsed atom data.
    - box (list): A list of floats representing the box dimensions.

    Example:
    >>> data, box = read_gro('md_nowater.gro', test=True, random_test_num=15)
    >>> print(data)
    >>> print(box)
    """
    with open(file_path, 'r') as file:
        # 忽略第1行
        file.readline()
        
        # 读取第2行，获取总数 x
        x = int(file.readline().strip())
        
        # 初始化存储数据的列表
        data = []
        
        # 读取接下来的 x 行
        for _ in range(x):
            line = file.readline()
            
            # 按照固定格式解析每一行
            res_id = int(line[0:5].strip())
            res_name = line[5:10].strip()
            atom_name = line[10:15].strip()
            atom_id = int(line[15:20].strip())
            position_x = float(line[20:28].strip())
            position_y = float(line[28:36].strip())
            position_z = float(line[36:44].strip())
            speed_x = float(line[44:52].strip())
            speed_y = float(line[52:60].strip())
            speed_z = float(line[60:68].strip())
            
            # 将解析后的数据存储到列表中
            data.append({
                'res_id': res_id,
                'res_name': res_name,
                'atom_name': atom_name,
                'atom_id': atom_id,
                'position_x': position_x,
                'position_y': position_y,
                'position_z': position_z,
                'speed_x': speed_x,
                'speed_y': speed_y,
                'speed_z': speed_z
            })
        
        # 读取最后一行，解析 box
        box_line = file.readline().strip()
        box = list(map(float, box_line.split()))
        df = pd.DataFrame(data)
        
        # 如果 test 参数为 True，则调用 test_gro
        if test:
            test_gro(file_path, random_test_num=random_test_num)
        
        return df, box

def test_gro(file_path, random_test_num=10):
    """
    Validates the correctness of the `read_gro` function by comparing random lines.

    Parameters:
    - file_path (str): The path to the .gro file to be tested.
    - random_test_num (int): The number of random lines to validate.

    Returns:
    - None: Prints validation results to the console.

    Example:
    >>> test_gro('md_nowater.gro', random_test_num=5)
    """
    # 调用 read_gro 函数解析文件，获取总行数 x
    with open(file_path, 'r') as file:
        file.readline()  # 跳过第 1 行
        x = int(file.readline().strip())  # 获取总行数
    
    # 随机生成行号
    start_line = 2  # 第 3 行的索引
    end_line = min(9999, x)  # 确保不超过文件的实际行数
    random_lines = sorted(random.sample(range(start_line, end_line), random_test_num))  # 排序行号以便逐行读取
    print("随机生成的行号:", random_lines)
    
    # 初始化 DataFrame 和解析结果
    df, _ = read_gro(file_path)
    
    # 打开文件逐行读取，仅处理指定行号
    with open(file_path, 'r') as file:
        file.readline()  # 跳过第 1 行
        file.readline()  # 跳过第 2 行
        
        current_line = 2  # 当前行号（从第 3 行开始）
        for line in file:
            if current_line in random_lines:
                # 按空格分隔字符串
                parts = line.strip().split()
                
                # 解析分隔出的内容
                res = parts[0]
                atom_name = parts[1]
                atom_id = int(parts[2])
                position_x = float(parts[3])
                position_y = float(parts[4])
                position_z = float(parts[5])
                speed_x = float(parts[6])
                speed_y = float(parts[7])
                speed_z = float(parts[8])
                
                # 从 DataFrame 中获取对应行
                df_row = df.iloc[current_line - 2]  # DataFrame 索引从 0 开始
                
                # 对比解析结果与 DataFrame 中的值
                assert res == str(df_row['res_id']) + df_row['res_name'], f"行 {current_line} 的 res 不匹配"
                assert atom_name == df_row['atom_name'], f"行 {current_line} 的 atom_name 不匹配"
                assert atom_id == df_row['atom_id'], f"行 {current_line} 的 atom_id 不匹配"
                assert position_x == df_row['position_x'], f"行 {current_line} 的 position_x 不匹配"
                assert position_y == df_row['position_y'], f"行 {current_line} 的 position_y 不匹配"
                assert position_z == df_row['position_z'], f"行 {current_line} 的 position_z 不匹配"
                assert speed_x == df_row['speed_x'], f"行 {current_line} 的 speed_x 不匹配"
                assert speed_y == df_row['speed_y'], f"行 {current_line} 的 speed_y 不匹配"
                assert speed_z == df_row['speed_z'], f"行 {current_line} 的 speed_z 不匹配"
                
                print(f"行 {current_line} 测试通过！")
            
            # 增加当前行号
            current_line += 1