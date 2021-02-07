from enum import Enum

# attempted port of following MIT licensed depot
# https://github.com/priyeshkpandey/emotions-simulation/tree/master/occ-java-wrapper/src/main/java/com/occ


class EmotionAspectConstraint(Enum):
    IsPresent = 1
    IsPositive = 2
    IsZero = 3
    IsNegative = 4


def get_constraint__is_present() -> dict:
    return {EmotionAspectConstraint.IsPresent: True}


def get_constraint__is_positive() -> dict:
    return {
          EmotionAspectConstraint.IsPresent: True
        , EmotionAspectConstraint.IsPositive: True
    }


def get_constraint__is_negative() -> dict:
    return {
          EmotionAspectConstraint.IsPresent: True
        , EmotionAspectConstraint.IsNegative: True
    }


class EmotionAspectRule(Enum):
    # global?
    Unexpectedness = 1
    SenseOfReality = 2
    Proximity = 3
    Arousal = 4
    Valance = 5

    # event?
    Desirability = 6
    # event for others
    Deservingness = 7
    Liking = 8 # wtf even is this?
    DesirabilityForOther = 9
    # event future
    Likelihood = 10
    # event present
    Realization = 11
    Effort = 12

    # object
    Appealingness = 13
    Familiarity = 14

    # agent action
    Praisworthyness = 15
    PersonalIntegrity = 16
    ExpectationDeviation = 17


def get_rule__global_variables_present() -> dict:
    return {
          EmotionAspectRule.Unexpectedness: get_constraint__is_present()
        , EmotionAspectRule.SenseOfReality: get_constraint__is_present()
        , EmotionAspectRule.Arousal: get_constraint__is_present()
        , EmotionAspectRule.Proximity: get_constraint__is_present()
    }


def get_rule__happily_desired_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
            , EmotionAspectRule.Deservingness: get_constraint__is_positive()
            , EmotionAspectRule.Liking: get_constraint__is_positive()
            , EmotionAspectRule.DesirabilityForOther: get_constraint__is_positive()
        }
    )
    return rule


# envy?
def get_rule__resented_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
            , EmotionAspectRule.Deservingness: get_constraint__is_negative()
            , EmotionAspectRule.Liking: get_constraint__is_negative()
            , EmotionAspectRule.DesirabilityForOther: get_constraint__is_positive()
        }
    )
    return rule


# sorry for experience
def get_rule__apologetic_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
            , EmotionAspectRule.Liking: get_constraint__is_positive()
            , EmotionAspectRule.Deservingness: get_constraint__is_negative()
            , EmotionAspectRule.DesirabilityForOther: get_constraint__is_negative()
        }
    )
    return rule


def get_rule__gloating_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
            , EmotionAspectRule.Liking: get_constraint__is_negative()
            , EmotionAspectRule.Deservingness: get_constraint__is_positive()
            , EmotionAspectRule.DesirabilityForOther: get_constraint__is_negative()
        }
    )
    return rule


def get_rule__hopeful_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
        }
    )
    return rule


def get_rule__feared_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
        }
    )
    return rule


def get_rule__satisfying_experience() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
            , EmotionAspectRule.Realization: get_constraint__is_positive()
            , EmotionAspectRule.Effort: get_constraint__is_present()
        }
    )
    return rule


def get_rule__fears_confirmed() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
            , EmotionAspectRule.Realization: get_constraint__is_positive()
            , EmotionAspectRule.Effort: get_constraint__is_present()
        }
    )
    return rule


def get_rule__is_relieving() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
            , EmotionAspectRule.Realization: get_constraint__is_negative()
            , EmotionAspectRule.Effort: get_constraint__is_present()
        }
    )
    return rule


def get_rule__is_disappointing() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
            , EmotionAspectRule.Likelihood: get_constraint__is_positive()
            , EmotionAspectRule.Realization: get_constraint__is_negative()
            , EmotionAspectRule.Effort: get_constraint__is_present()
        }
    )
    return rule


def get_rule__is_joyful() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_positive()
        }
    )
    return rule


def get_rule__is_distressing() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Desirability: get_constraint__is_negative()
        }
    )
    return rule


def get_rule__is_prideful() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Praisworthyness: get_constraint__is_positive()
            , EmotionAspectRule.PersonalIntegrity: get_constraint__is_positive()
            , EmotionAspectRule.ExpectationDeviation: get_constraint__is_present()
        }
    )
    return rule


def get_rule__is_shameful() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Praisworthyness: get_constraint__is_negative()
            , EmotionAspectRule.PersonalIntegrity: get_constraint__is_positive()
            , EmotionAspectRule.ExpectationDeviation: get_constraint__is_present()
        }
    )
    return rule


def get_rule__is_admirable() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Praisworthyness: get_constraint__is_positive()
            , EmotionAspectRule.ExpectationDeviation: get_constraint__is_positive()
        }
    )
    return rule


def get_rule__is_reprehensible() -> dict:
    rule = get_rule__global_variables_present()
    rule.update(
        {
              EmotionAspectRule.Praisworthyness: get_constraint__is_negative()
            , EmotionAspectRule.ExpectationDeviation: get_constraint__is_positive()
        }
    )
    return rule











class Rule:
    def __init__(self):
        self.rules = {}

    def add_aspect(self, aspect, constraint):
        if aspect not in self.rules:
            self.rules[aspect] = constraint


class Emotion:
    def __init__(self, name, rule, potential, intensity, threshold):
        self.name = name
        self.rule = rule
        self.potential = potential
        self.intensity = intensity
        self.threshold = threshold



