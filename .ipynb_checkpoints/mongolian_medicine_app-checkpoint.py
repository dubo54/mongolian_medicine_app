import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
from PIL import Image
import io

# 设置页面标题
st.set_page_config(page_title="蒙药数据库查询系统", layout="wide")

# 加载数据
@st.cache_data
def load_data():
    file_path = "D:\\mysjk\\mongolian_medicine_data_test.csv"
    df = pd.read_csv(file_path)
    return df

df = load_data()

# 定义函数来获取化合物结构式图像
def get_structure_image(smiles):
    try:
        # 使用 RDKit 将 SMILES 转换为分子对象
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            # 生成分子结构式图像
            img = Draw.MolToImage(mol)
            return img
        else:
            st.error("无法从SMILES生成分子结构")
    except Exception as e:
        st.error(f"获取结构式图像时出错: {e}")
    return None

# 创建查询界面
st.title("蒙药数据库查询系统")
st.write("请输入查询条件:")

# 创建查询条件选择
query_type = st.selectbox("选择查询条件类型:", [
    "ESI_Ion Mode_Plus", "ESI_Calcm/z_Plus", "ESI_Fragment ions(m/z)_Plus",
    "ESI_Ion Mode_Minus", "ESI_Calcm/z_Minus", "ESI_Fragment ions(m/z)_Minus"
])

# 根据查询类型创建输入框
if query_type in ["ESI_Ion Mode_Plus", "ESI_Ion Mode_Minus"]:
    query_value = st.selectbox("选择值:", ["[M-H]-", "[M+H]+", "[2M-H]-", "-"])
else:
    query_value = st.text_input("输入值:")

# 查询按钮和重置按钮
query_button = st.button("查询")
reset_button = st.button("重置")

# 处理重置按钮
if reset_button:
    st.experimental_rerun()

# 执行查询
if query_button:
    # 根据查询类型和值筛选数据
    if query_type in ["ESI_Ion Mode_Plus", "ESI_Ion Mode_Minus"]:
        results = df[df[query_type] == query_value]
    else:
        # 转换为字符串进行比较
        results = df[df[query_type].astype(str).str.contains(query_value)]

    # 显示结果
    if not results.empty:
        st.success(f"找到 {len(results)} 条记录")
        for index, row in results.iterrows():
            st.subheader(f"ID: {row['ID']}")
            st.write(f"化合物名称: {row['Compound Name']}")
            st.write(f"分子式: {row['Formula']}")
            st.write(f"CAS 号: {row['CAS']}")
            st.write(f"SMILES: {row['SMILES']}")
            st.write(f"化合物类别: {row['Compound Class']}")
            st.write(f"来源: {row['Compound Source']}")
            st.write(f"参考: {row['Reference']}")
            st.write(f"备注: {row['Remark']}")
            
            # 显示结构式图像
            st.write("结构式:")
            image = get_structure_image(row['SMILES'])
            if image:
                st.image(image, use_container_width=True)  # 修改后的代码
            else:
                st.write("无法获取结构式图像")
            
            st.markdown("---")
    else:
        st.warning("未找到符合条件的记录")