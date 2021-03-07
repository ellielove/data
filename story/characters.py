from enum import Enum


class CharacterType(Enum):
    Role = 'Role'
    Species = 'Species'
    PhysicalAttribute = 'PhysicalAttribute'
    MentalAttribute = 'MentalAttribute'
    BehaviouralAttribute = 'BehaviouralAttribute'
    SkillCapability = 'SkillCapability'
    Aesthetic = 'Aesthetic'


class Role(Enum):
    Cleric = 'Cleric'
    Companion = 'Companion'
    EnforcerHurter = 'EnforcerHurter'
    Hero = 'Hero'
    Judge = 'Judge'
    Lawbreaker = 'Lawbreaker'
    Leader = 'Leader'
    Messenger = 'Messenger'
    MoneyOwner = 'MoneyOwner'
    Prophet = 'Prophet'
    Rival = 'Rival'
    Seeker = 'Seeker'
    Shopkeeper = 'Shopkeeper'
    Student = 'Student'
    TrueFriend = 'TrueFriend'
    Villain = 'Villain'


class Species(Enum):
    Giant = 'Giant'
    Minotaur = 'Minotaur'
    Golem = 'Golem'
    Dog = 'Dog'
    Cat = 'Cat'
    Cow = 'Cow'
    Demon = 'Demon'


class PhysicalAttribute(Enum):
    Deaf = 'Deaf'
    Blind = 'Blind'
    ShockinglyBig = 'ShockinglyBig'
    ShockinglySmall = 'ShockinglySmall'
    Twins = 'Twins'
    Skeleton = 'Skeleton'
    Ghost = 'Ghost'


class MentalAttriubtue(Enum):
    a = 1


class BehaviouralAttribute(Enum):
    Wanderer = 'Wanderer'
    Nudist = 'Nudist'


class SkillCapability(Enum):
    Mage = 'Mage'


class Aesthetic(Enum):
    Cowpoke = 'Cowpoke'
    Cyberpunk = 'Cyberpunk'
    Apocalypse = 'Apocalypse'
    Zombie = 'Zombie'


def get_character_dict() -> dict:
    return {

          CharacterType.Role: {
              Role.Cleric: {}
            , Role.Companion: {}
            , Role.EnforcerHurter: {}
            , Role.Hero: {}
            , Role.Judge: {}
            , Role.Lawbreaker: {}
            #, Role.Layer: {}
            , Role.Leader: {}
            , Role.Messenger: {}
            , Role.MoneyOwner: {}
            #, Role.Professor: {}
            , Role.Prophet: {}
            , Role.Rival: {}
            , Role.Seeker: {}
            , Role.Shopkeeper: {}
            #, Role.Skillworker: {}
            , Role.Student: {}
            , Role.TrueFriend: {}
            , Role.Villain: {}
        }

        , CharacterType.Species: {
        }

        , CharacterType.PhysicalAttribute: {
              PhysicalAttribute.Blind: {}
            , PhysicalAttribute.Deaf: {}
            , PhysicalAttribute.ShockinglyBig: {}
            , PhysicalAttribute.ShockinglySmall: {}
            , PhysicalAttribute.Twins: {}
            , PhysicalAttribute.Skeleton: {}
            , PhysicalAttribute.Ghost: {}
        }

        , CharacterType.MentalAttribute: {
        }

        , CharacterType.BehaviouralAttribute: {
        }

        , CharacterType.SkillCapability: {
              SkillCapability.Mage: {}
        }

        , CharacterType.Aesthetic: {
              Aesthetic.Cowpoke: {}
            , Aesthetic.Cyberpunk: {}
            , Aesthetic.Apocalypse: {}
            , Aesthetic.Zombie: {}
        }


    }


