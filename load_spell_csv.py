import sys
from typing import Optional

import pandas as pd

from src.schemas.resources import Spell, SpellSchool, SpellComponent


# 辅助函数：将字符串转换为布尔值
def bool_from_str(val: str) -> bool:
    return val.strip() == "√"

# 中文学派映射到英文版学派
SCHOOL_MAPPING = {
    "幻术": SpellSchool.ILLUSION,
    "惑控": SpellSchool.ENCHANTMENT,
    "预言": SpellSchool.DIVINATION,
    "变化": SpellSchool.TRANSMUTATION,
    "塑能": SpellSchool.EVOCATION,
    "死灵": SpellSchool.NECROMANCY,
    "防护": SpellSchool.ABJURATION,
    "咒法": SpellSchool.CONJURATION,
}

# CSV中定义的职业列
CLASS_MAPPING = {
    "吟游诗人": "Bard",
    "牧师": "Cleric",
    "德鲁伊": "Druid",
    "圣武士": "Paladin",
    "游侠": "Ranger",
    "术士": "Sorcerer",
    "魔契师": "Warlock",
    "法师": "Wizard",
    "奇械师": "Artificer",
    "时间": "Chronurgy",
    "重力": "Graviturgy ",
}

COMPONENT_MAPPING = {
    "V 言语": SpellComponent.V,
    "S 姿势": SpellComponent.S,
    "M 材料": SpellComponent.M,
}

# 解析 CSV 行并转换为 Spell 对象
def parse_spell(row: dict) -> Optional[Spell]:
    # 将 CSV 中中文列映射到对应的 Spell 字段
    name = row['法术名']
    level = int(row['环阶']) if row["环阶"] != float("nan") else 0
    school = SCHOOL_MAPPING.get(row['学派'], SpellSchool.UNCLASSIFIED)
    casting_time = row['施法时间']
    spell_range = row['施法距离']
    comps = [value for key, value in COMPONENT_MAPPING.items() if row.get(key, "") == value]
    duration = row['持续时间']
    description = row['法术详述']
    ritual = bool(row.get('仪式', ''))
    concentration = bool(row.get('专注', ''))
    # 填充 classes 字段，检查每个预定义职业列是否标记为 "√"
    classes = [cls_en for cls_cn, cls_en in CLASS_MAPPING.items() if row.get(cls_cn, "") == "√"]
    return Spell(
        name=name,
        level=level,
        school=school,
        casting_time=casting_time,
        range=spell_range,
        components=comps,
        duration=duration,
        description=description,
        ritual=ritual,
        concentration=concentration,
        classes=classes
    )


if __name__ == "__main__":
    csv_file = "data/dnd2024spell.csv"  # 替换为实际的 CSV 文件路径
    df = pd.read_csv(csv_file, encoding='utf-8')
    rows = df.iterrows()
    spells = [parse_spell(row) for _, row in rows]
    for spell in spells:
        print(spell.model_dump_json())
