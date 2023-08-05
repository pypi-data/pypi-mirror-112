# pySCIL
New deployment of the SCIL toolset using NLP tools from Python

The Socio-cultural Content in Language (SCIL) toolset intents to explore and develop novel designs, algorithms, methods, techniques and technologies to extend the discovery of the social goals of members of a group by correlating these goals with the language they use. (description via IARPA)

# Installation

The following are instructions on how to install pySCIL from PyPI.

Type the following in your terminal. Make sure you are using Python 3.6+

`pip install pySCIL`

# Usage
Include the above imports at the top of your program file
```python
import json
from scil import scil
```
To begin analyzing a dialogue type the following code
```python
with open("pathtojson.json") as f:
  obj = scil.SCIL(f)
obj.preprocessStanford()
```
Make sure that your json file is formatted properly. An example can be seen in the `jsontemplate.json` file

Currently, only the Stanford Part of Speech tagger is supported but in the future you would also be able to do analysis using `obj.preprocessNLTK()`

From here, you can now start to call functions to do analysis on the data. See below functions section for more details. As an example.
```python
print(obj.TopicControlFunctions([1,0.5,0.5,0.5]))
```

# Functions
Each service has a main function that gathers data from all sub-functions and creates a combined metric. These sub-functions can also be called individually. Below are all the callable functions outlined along with what sort of data they require to be present in the provided json file.

- TopicControlFunctions(weights)
  - weights are optional and default to [1,1,1,1]
  - LocalTopicIntroduction()
  - SubsequentMentionsLocalTopics()
  - CiteScore()
  - TurnLength()
- TaskControlFunctions(weights)
  - weights are optional and default to [1,1,1]
  - DirectiveIndex()
    - requires "dialog_act" tags
  - ProcessManagementIndex()
    - requires "dialog_act" metaTags
  - ProcessManagementSuccessIndex()
    - requires "dialog_act" tags and metaTags
    - requires "link_to"
- ArgumentDiversityFunctions(weights)
  - weights are optional and default to [1,1]
  - VocabularyRangeIndex()
  - VocabularyIntroductionMeasure()
- TopicalPositioningFunctions()
  - TopicalPolarityIndex()
    - requires "dialog_act" tags
    - requires "polarity"
    - requires "turn_no"
    - requies "link_to"
  - PolarityStrengthIndex()
    - requires "dialog_act" tags
    - requires "polarity"
    - requires "turn_no"
    - requies "link_to"
- AgreementFunctions(weights)
  - weights are optional and default to [1,1]
  - AgreeAcceptIndex()
    - requires "dialog_act" tags
  - TopicalAgreementIndex()
    - requires "topic"
    - requires "polarity"
    - requires "dialog_act" tags
- DisagreementFunctions(weights)
  - weights are optional and default to [1,1]
  - DisagreeRejectIndex()
    - requires "dialog_act" tags
  - TopicalDisagreementIndex
    - requires "topic"
    - requires "polarity"
    - requires "dialog_act" tags
- EmotiveLanguageUseFunctions(weights)
  - weights are optional and default to [1]
  - this service currently only has one sub-function
  - EmotiveWordIndex()
- SocialPositioningFunctions(weights)
  - weights are optional and default to [1,1]
  - OfferCommitIndex()
    - requires "dialog_act" tags
  - ConfirmationRequestIndex()
    - requires "dialog_act" tags
- SociabilityFunctions(weights)
  - weights are optional and default to [1,1,1,1]
  - ConversationalNormsMeasure()
    - requires "dialog_act" tags
    - requires "link_to"
    - requires "comm_act_type"
  - AgreementDisagreementMeasure()
    - requires "dialog_act" tags
  - NetworkDensityIndex()
    - requires "comm_act_tag"
  - CiteDisparityIndex()
    - requires "link_to"
- InvolvementFunctions(weights)
  - weights are optional and default to [1,1,1,1,1]
  - NounPhraseIndex()
  - TurnIndex()
  - TopicChainIndex(gapSizeCutoff, mentionPercentageFloor)
    - a new topic will be created if last mention was more than gapSizeCutoff turns ago (defaults to 10)
    - only topics with at least mentionPercentageFloor of mentions will be included as top topics (defaults to 0.05 as in 5%)
    - requires "turn_no"
  - AllSubsequentMentions()
  - AllotopicalityIndex()
- NetworkCentralityFunctions(weights)
  - weights are optional and default to [1,1]
  - CommunicationLinksMeasure
    - requires "link-to"
  - MesoTopicIntroduction()
- TaskFocusFunctions(weights)
  - weights are optional and default to [1,1]
  - MesoTopicStructureMeasure()
  - MesoTopicGappingMeasure()
- TensionFocusFunctions(weights)
  - weights are optional and default to [1,1]
  - DisagreeRejectTargetIndex()
    - requires "link_to"
    - requires "dialog_act" tags
  - TopicalDisagreementTargetIndex()
    - requires "link_to"
    - requires "topic"
    - requires "polarity"
- Leadership(topicControlScores, taskControlScores, involvementScores, disagreementScores, weights)
  - weights are optional and default to [0.45,0.4,0.05,0.1]
  - all scores are the output of the <service>Functions() functions
- Influencer(argumentDiversityScores, networkCentralityScores, topicControlScores, disagreementScores, weights)
  - weights are optional and default to [0.4,0.5,0.75,0.15]
- PursuitOfPower(topicControlScores, disagreementScores, tensionFocusScores, networkCentralityScores, weights)
  - weights are optional and default to [0.8,0.09,0.02,0.09]
- GroupCohesion(topicControlScores, taskControlScores, involvementScores, agreementScores, disagreementScores, sociabilityScores, taskFocusScores, sociabilityThreshold, taskFocusTreshold, prmMesoTopicFloor, prmDialogueFloor, prmThreshold, prmWeights, dpmThreshold)
  - sociabilityThreshold defaults to 0.68. If sociability is at least threshold, add 0.25 to GroupCohesion
  - taskFocusThreshold defaults to 0.32. If taskFocus is at least threshold, add 0.25 to GroupCohesion
  - prmMesoTopicFloor defaults to 3. PRM ignores conversations with less than 3 meso topics (unless it has more than 150 utterances)
  - prmDialogueFloor defaults to 150. PRM ignores conversations with less than 150 utterances (unless it has at least 3 meso topics)
  - prmThreshold defaults to 0.75. If PRM is at least threshold, add 0.25 to GroupCohesion
  - prmWeights is optional and defaults to [1,0.9,0.3,0.7,0.7]. The weights are for topicControl, taskControl, involvement, agreement, disagreement
  - dpmThreshold defaults to 0.69. If DPM is at least threshold, add 0.25 to GroupCohesion
    
  
# Services

## Agenda Control Class
### Topic Control
Attempts by a discourse participant or participants to impose the topic of conversation.
### Task Control
The effort by one or more members of a group to define the group's project goal and/or steer the group towards it.
### Argument Diversity
Displayed by speakers who deploy a broader range of arguments in conversation.
### Topical Positioning
The attitude a speaker has on main the topics (meso-topics) of discussion.

## Interpersonal Relations Class
### Agreement
Signaled when discourse participants make explicit, unqualified utterances of agreement, approval, or acceptance in response to a prior speaker's utterance.
### Disagrement
Signaled when discourse participants make explicit, utterances of disagreement, disapproval, or rejection in response to a prior speaker's utterance.
### Emotive Language Use
Defined as a degree to which speakers attempt to influence readers or listeners by appealing to their emotions.
### Social Positioning
Defined as a degree to which the speaker attempts to position oneself as central in the group by committing to some future activity and by getting others to confirm or re-affirm what the speaker stated or committed to, as well as what the speaker already believes.
### Sociability
Defined as a degree of socio-emotional involvement between speakers, including observance of group conversational norms.

## Participation and Engagement Class
### Involvement
Defined as a degree of engagement or participation in the discussion of a group.
### Network Centrality
Defined as the degree to which a speaker is someone to whom others direct their comments and/or whose topics they cite.
### Task Focus
Defined as a degree to which speakers remain engaged in a group task.
### Tension Focus
Defined as the degree to which a speaker is someone at whome others direct their disagreement, or with whose topics they disagree the most.

### ** WIP **
