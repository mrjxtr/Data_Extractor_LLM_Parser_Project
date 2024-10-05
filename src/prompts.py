CLINICAL_TRIAL_PROMPT = """
Make sure to read every instruction and follow it exactly.

I am giving you text that is intended to have clinical trial results data.

I am also going to give you a series of questions, and I want you to answer the questions number by number. Do not restate the question, simply give the answer with the corresponding number from the question. If there is not an applicable answer you can just leave an “NA”

Provide the set of answers to the questions for ALL clinical trials that are provided. Keep each set of answers for each clinical trial separate. If there is more than one clinical trial then you should give multiple lists that start over from #1 for each clinical trial.

Be as concise as possible while being complete

It is important that you follow the format exactly as it is given.

It is important that when giving your response, you just go straight to the answer, do not restate the question or give any other commentary.

When asked for mutations, targets, biomarkers, genes etc simply give the acronym for the mutation. When asked for biomarkers simply give the biomarker. When listing drugs keep it as concise as you can, do not list the drug brand name, only the drug name.

When listing secondary or sensitizing mutations, be sure to ONLY list the secondary mutations, do not list the primary mutations if it is just the secondary or sensitizing mutations that apply. For Example: “EGFR TKI sensitizing mutation (Exon 19 deletion or L858R mutation)” You should only list: Exon 19 deletion, L858R)

When listing any mutations, targets, biomarkers,genes, be careful not to list the inverse of what I ask. For instance if I ask Which patient Mutation(s) enrolled/studied in the trial, DO NOT  list the mutations which did not participate in your answer. For example do not say “No EGFR”, “no ALK” etc. We will be using these terms to match a criteria and we don't want the inverse what is intended to ever match.

When you give your response, you should restate the question on the number item, then give the answer on the next line with an #A.

First do the “Trial Identification” phase so we can identify the clinical trials. This is primarily done incase there is more than one clinical trial on the page.

1. How many Clinical Trials are there? (This should equal the number of Traial names or titles I will give you)

Replace "Insert Trial Name Here" with a concise version of the Trial title or "title". Avoid using commas or colons for the Trial Name.
For Example:

Trial1-Info:NCT#:Insert Trial Name Here:#ofPatients
Trial2-Info:NCT#:Insert Trial Name Here:#ofPatients
Trial3-Info:NCT#:Insert Trial Name Here:#ofPatients

Example clinical trial:
"title": "Voice-Activated Cognitive Behavioral Therapy for Insomnia: A Randomized Clinical Trial",
"abstract": "Importance:                    Insomnia symptoms affect an estimated 30% to 50% of the 4 million US breast cancer survivors. Previous studies have shown the effectiveness of cognitive behavioral therapy for insomnia (CBT-I), but high insomnia prevalence suggests continued opportunities for delivery via new modalities.              Objective:                    To determine the efficacy of a CBT-I-informed, voice-activated, internet-delivered program for improving insomnia symptoms among breast cancer survivors.              Design, setting, and participants:                    In this randomized clinical trial, breast cancer survivors with insomnia (Insomnia Severity Index [ISI] score >7) were recruited from advocacy and survivorship groups and an oncology clinic. Eligible patients were females aged 18 years or older who had completed curative treatment more than 3 months before enrollment and had not undergone other behavioral sleep treatments in the prior year. Individuals were assessed for eligibility and randomized between March 2022 and October 2023, with data collection completed by December 2023.              Intervention:                    Participants were randomized 1:1 to a smart speaker with a voice-interactive CBT-I program or educational control for 6 weeks.              Main outcomes and measures:                    Linear mixed models and Cohen d estimates were used to evaluate the primary outcome of changes in ISI scores and secondary outcomes of sleep quality, wake after sleep onset, sleep onset latency, total sleep time, and sleep efficiency.              Results:                    Of 76 women enrolled (38 each in the intervention and control groups), 70 (92.1%) completed the study. Mean (SD) age was 61.2 (9.3) years; 49 (64.5%) were married or partnered, and participants were a mean (SD) of 9.6 (6.8) years from diagnosis. From baseline to follow-up, ISI scores changed by a mean (SD) of -8.4 (4.7) points in the intervention group compared with -2.6 (3.5) in the control group (P < .001) (Cohen d, 1.41; 95% CI, 0.87-1.94). Sleep diary data showed statistically significant improvements in the intervention group compared with the control group for sleep quality (0.56; 95% CI, 0.39-0.74), wake after sleep onset (9.54 minutes; 95% CI, 1.93-17.10 minutes), sleep onset latency (8.32 minutes; 95% CI, 1.91-14.70 minutes), and sleep efficiency (-0.04%; 95% CI, -0.07% to -0.01%) but not for total sleep time (0.01 hours; 95% CI, -0.27 to 0.29 hours).              Conclusions and relevance:                    This randomized clinical trial of an in-home, voice-activated CBT-I program among breast cancer survivors found that the intervention improved insomnia symptoms. Future studies may explore how this program can be taken to scale and integrated into ambulatory care.              Trial registration:                    ClinicalTrials.gov Identifier: NCT05233800.",
"url": "https://pubmed.ncbi.nlm.nih.gov//39316400/"

"title": "Acellular Dermal Matrix, without Basement Membrane in Immediate Prepectoral Breast Reconstruction: A Randomized Controlled Trial",
"abstract": "Background:                    Acellular dermal matrix (ADM) has become popular in various reconstructive procedures of different anatomic regions. There are different needs depending on the clinical application, including breast, abdominal wall, and any other soft-tissue reconstruction. Removal of the basement membrane, which consists of collagen fibers, may help achieve natural and soft breast reconstruction, which requires highly elastic ADMs. Given the lack of knowledge of the effectiveness of ADM without the basement membrane, the authors compared the clinical outcomes of ADMs with and without basement membrane in breast reconstruction.              Methods:                    The authors conducted a single-blind randomized controlled trial to evaluate differences in clinical outcomes. The patients were randomized into 2 groups: ADM with or without basement membrane. Both groups underwent immediate prepectoral direct-to-implant breast reconstruction. Demographic characteristics, surgical outcomes, and breast shape change using nipple position were compared between the 2 groups.              Results:                    A total of 56 patients were divided into 2 groups: ADM with basement membrane (n = 30 [53.6%]) or ADM without basement membrane (n = 26 [46.4%]). Clinical and surgical characteristics were similar between the 2 groups. The authors detected no statistically significant differences in the overall rate of complications or breast shape change between the 2 groups. However, the rate of seromas was higher in the ADM with basement membrane group than in the ADM without basement membrane group (10% versus 0%; P = 0.09).              Conclusions:                    The 2 groups showed similar surgical outcomes. ADM without basement membrane in implant-based breast reconstruction was safe, and had mechanical properties of lower tensile strength and higher elasticity.              Clinical question/level of evidence:                    Therapeutic, II.",
"url": "https://pubmed.ncbi.nlm.nih.gov//39314097/"

Example output:
Trial1-Info:NCT05233800:Voice-Activated Cognitive Behavioral Therapy for Insomnia:70
Trial2-Info:NA:Acellular Dermal Matrix without Basement Membrane in Immediate Prepectoral Breast Reconstruction:56

(If there is 10 total trial titles then the output should be 10 lines, Trial1-Info:N..., Trial2-Info:N..., Trial3-Info:N...etc.)
(If there is no NCT# or no number of patients, participants, or something of that nature then you should put NA)

Next answer “Trial Questions”:

Important: You should only answer questions for the trial that you defined as Trial 1 on this pass. If there are other trials they will be follow up prompts done for those trials.


1. What is the NCT# Associated with this clinical trial? (If there is one)
2. What Phase is the clinical trial in? Phase 1, Phase 2, Phase 3, or Phase 4?
3. What type of cancer(s) was this trial studying? ie- NSCLC, SCLC, Melanoma, Leukemia, Colon etc
4. Describe the Cancer Type?
5. Who sponsored the clinical trial?
6. What were the novel findings of this trial?
7. What conclusions were reached regarding this clinical trial?
8. Is there any other relevant information that might make this clinical trial unique? (Try to keep this somewhat concise)
9. Were there any subgroups in this study that the clinical trial identified had heightened responses to the intervention?

Next you should define the “Study Groups” and then answer the “Group Questions”:

To define the “Study Groups”: How many study groups are there? If subgroup analysis or subgroup efficacy analysis is done (such as based on targets, mutations or prior treatments etc) they should receive their own group as well.Give each group a Name - for example -

Group1:ControlGroup—DrugNames(s)—UniqueCharacteristics
Group2:InterventionGroup—DrugName(s)—UniqueCharacteristics
Group3:InterventionGroup—DrugName(s)—UniqueCharacteristics
…

Once you've defined the groups, Answer the following questions about each cohort/group/treatment arm by using their Group# Identifier. This should be done for all groups from the “Study Groups”. X should be replaced with the Group number:

Group Questions:

GroupX-1. Is this the control group or the intervention group?
GroupX-2. What drug(s) was the clinical trial studying in the this group/cohort?
GroupX-3. What was the Treatment ORR in this group/cohort?
GroupX-4. What was the Intervention Treatment PFS in this group/cohort?
GroupX-5. What was the Intervention Treatment OS in this group/cohort?
GroupX-6. What percentage of patients In the intervention group discontinued?
GroupX-7. Did the Group Specifically meet its endpoints? Yes or No or NA
GroupX-8. Did the Group Specifically include patients who had specific stages of cancer? If so, what stages?
GroupX-9. Did the Group include patients who had targets? (such as mutations, biomarkers, genes, etc)
GroupX-10. Did the Group Specifically include patients who had previously taken a specific drug type?
GroupX-11. Did the Group Specifically include patients who had specifically developed resistance to specific drugs? If so, List the drugs
GroupX-12. Did the Group Specifically include patients who had specifically developed resistance to specific drug types? If so,  List the drug types
GroupX-13. Did the Group Specifically include patients who had brain brain metastases? Yes or No
GroupX-14. Did the Group Specifically include patients who had previous surgery? Yes or No
GroupX-15. Did the Group Specifically include patients who had “advanced” cancer? Yes or No
GroupX-16. Did the Group Specifically include patients who had “metastatic” cancer? Yes or No
GroupX-17. Did the Group Specifically include patients who were previously untreated?
GroupX-18. Did the Group Specifically include patients who had previously taken a specific drug? If so, List the drugs
GroupX-19. Did the Group Specifically include patients who had NOT previously taken a specific drug? If so, List the drugs
GroupX-20. Did the Group specifically include patients who were receiving a 1st,2nd,3rd,4th,5th… Therapy? Please Specify
GroupX-21. Was the treatment for this group well tolerated?
GroupX-22. Were the specific adverse reactions associated with this group?
GroupX-23. Has the intervention drug(s) for this group been approved? Yes, No, or NA
GroupX-24. What other efficacy data points were measured? (ie- TTP, DoR, CR, PR, SD, CBR, pCR etc) Give in the format TTP:X, DoR:X, CR:X

It is important that your answer should be a compbination alf all the information from the clinical trial results information that will be given and format it into the following structure making all information from all trials available in this one response.
You should there should only be one set of Trial Identification, Trial Questions, Study Groups, and Group Questions in your response that contains all the information from all the trials.
The structure needs to be exact so it can be easily parsed:

Trial Identification:

1. How many Clinical Trials are there?
1A. [Answer]

Trial1-Info:NCT#:Insert Trial Name Here:#ofPatients
Trial2-Info:NCT#:Insert Trial Name Here:#ofPatients
Trial3-Info:NCT#:Insert Trial Name Here:#ofPatients

(Trial Info should be saved on one line for easier parsing and should be prefaced by the Trial# defined, and you should follow the exact format with colons for reliable parsing)
…


Trial Questions:
1.[Question Restated]
1A.[Answer]
2.[Question Restated]
2A.[Answer]
…

Study Groups:
Group1:ControlGroup:DrugNames(s):UniqueCharacteristics
Group2:InterventionGroup:DrugName(s):UniqueCharacteristics
Group3:InterventionGroup:DrugName(s):UniqueCharacteristics
(Study Group Info should be saved on one line for easier parsing, and should be prefaced with the group # so the groups can be parsed accordingly)
…

Group Questions: Maintain this exact format, but replace the # with the relevant Group # that you defined in the "Study Groups")

Group#-1.[Question Restated]
Group#-1A.[Answer]
Group#-2.[Question Restated]
Group#-2A.[Answer]
Group#-3.[Question Restated]
Group#-3A.[Answer]
…

Below is the information that should contain the clinical trial results:


Trial Name or "title": {headline}
Trial Abstract or "abstract": {body}
"""
