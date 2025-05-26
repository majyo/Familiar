from enum import Enum
from pydantic import BaseModel, Field


class SpellComponent(str, Enum):
    V = "V"  # Verbal
    S = "S"  # Somatic
    M = "M"  # Material


class SpellSchool(str, Enum):
    ABJURATION = "Abjuration"
    CONJURATION = "Conjuration"
    DIVINATION = "Divination"
    ENCHANTMENT = "Enchantment"
    EVOCATION = "Evocation"
    ILLUSION = "Illusion"
    NECROMANCY = "Necromancy"
    TRANSMUTATION = "Transmutation"
    UNCLASSIFIED = "Unclassified"


class Spell(BaseModel):
    """
    Represents a spell in the game.
    """
    name: str = Field(..., title="Name")
    level: int = Field(..., ge=0, title="Spell Level", description="The level of the spell, where 0 is a cantrip.")
    school: SpellSchool = Field(..., title="Spell School", description="The school of magic to which the spell belongs.")
    casting_time: str = Field(..., title="Casting Time", description="The time it takes to cast the spell.")
    range: str = Field(..., title="Range", description="The range of the spell, such as 'Self', '30 feet', etc.")
    components: list[SpellComponent] = Field(..., title="Components", description="The components required to cast the spell, such as verbal (V), somatic (S), and material (M).")
    duration: str = Field(..., title="Duration", description="How long the spell lasts, such as 'Instantaneous', '1 minute', etc.")
    description: str = Field(..., title="Description", description="A description of what the spell does.")
    ritual: bool = Field(False, title="Ritual", description="Indicates if the spell can be cast as a ritual without using a spell slot.")
    concentration: bool = Field(False, title="Concentration", description="Indicates if the spell requires concentration to maintain.")
    classes: list[str] = Field(..., title="Classes", description="The classes that can cast this spell. Note. There are two special classes 'Chronurgy' and 'Graviturgy', which can only be used by Wizards with the appropriate subclass.")


if __name__ == "__main__":
    # Example usage
    example_spell = Spell(
        name="Fireball",
        level=3,
        school=SpellSchool.EVOCATION,
        casting_time="1 action",
        range="150 feet",
        components=[SpellComponent.V, SpellComponent.S, SpellComponent.M],
        duration="Instantaneous",
        description="A bright streak flashes from your pointing finger to a point you choose within range and then blossoms with a low roar into an explosion of flame.",
        ritual=False,
        concentration=False,
        classes=["Sorcerer", "Wizard"]
    )
    print(example_spell.model_json_schema())
