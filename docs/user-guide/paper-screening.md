# 📋 Paper Screening User Guide

> **Step-by-step guide for using the compensation research paper screening system**

## 🎯 Getting Started

### **What is Paper Screening?**

The paper screening system automatically identifies high-quality, clinically relevant compensation research papers from academic databases. It uses a three-stage filtering process to find the most valuable studies for physical therapy and biomechanics practice.

### **Who Should Use This Guide?**

- **Physical Therapists** seeking evidence-based compensation research
- **Researchers** conducting systematic reviews or literature searches
- **Students** learning about compensation patterns in human movement
- **Clinicians** looking for assessment and treatment protocols

## 🔍 Understanding the Three-Stage Process

### **Stage 1: Field Specialization (0-18 points)**
Filters papers based on relevance to compensation research in physical therapy and biomechanics.

**What it evaluates:**
- Journal impact and relevance to the field
- Presence of compensation-related keywords
- Anatomical relevance to common dysfunction areas
- Exclusion of non-relevant content

**Passing threshold:** ≥8 points

### **Stage 2: Research Quality (0-28 points)**
Assesses the methodological rigor and scientific quality of studies.

**What it evaluates:**
- Study design quality (RCTs score highest)
- Sample size adequacy
- Citation impact and influence
- Institution quality and collaboration

**Passing threshold:** ≥12 points

### **Stage 3: Compensation Relevance (0-30 points)**
Determines how well the paper addresses compensation patterns and mechanisms.

**What it evaluates:**
- Potential for 5WHY causal analysis
- Quality of assessment methods used
- Relevance of interventions to compensation
- Specificity of compensation pattern description

**Passing threshold:** ≥15 points

## 🚀 Quick Start Guide

### **Basic Usage**

```python
from paper_screener import CompensationPaperScreener

# Initialize the screener
screener = CompensationPaperScreener()

# Screen papers (default: 20 papers)
papers = screener.screen_papers(limit=20)

# View results
for paper in papers:
    print(f"Title: {paper['title']}")
    print(f"Score: {paper['total_score']}/76")
    print(f"Journal: {paper['journal']}")
    print("---")
```

### **Understanding Results**

Each screened paper includes:
- **Total Score:** Combined score from all three stages (maximum 76 points)
- **Stage Breakdown:** Individual scores for field, quality, and relevance
- **Metadata:** Authors, journal, year, DOI
- **Compensation Indicators:** Identified patterns and clinical markers

## 📊 Interpreting Quality Scores

### **Score Ranges**

**Exceptional Quality (65-76 points)**
- Highest priority for clinical application
- Strong evidence base
- Detailed compensation analysis
- Excellent methodology

**High Quality (50-64 points)**
- Standard clinical reference material
- Good evidence support
- Clear compensation patterns
- Solid methodology

**Moderate Quality (35-49 points)**
- Supplementary evidence
- Limited but useful information
- Basic compensation description
- Adequate methodology

**Below Threshold (<35 points)**
- Excluded from analysis
- Insufficient quality or relevance
- Limited clinical applicability

### **Score Interpretation Examples**

**Example 1: Score 68/76 (Exceptional)**
```yaml
Paper: "EMG analysis of hip abductor compensation patterns"
Breakdown:
  Field Score: 17/18 (excellent journal, perfect keywords)
  Quality Score: 25/28 (RCT design, good sample size)
  Relevance Score: 26/30 (detailed compensation analysis)

Clinical Value: Highest priority - use for treatment protocols
```

**Example 2: Score 42/76 (Moderate)**
```yaml
Paper: "General exercise therapy for hip pain"
Breakdown:
  Field Score: 12/18 (relevant journal, limited keywords)
  Quality Score: 18/28 (observational study, modest sample)
  Relevance Score: 12/30 (minimal compensation focus)

Clinical Value: Supplementary reference only
```

## 🎯 Customizing Your Search

### **Setting Quality Thresholds**

```python
# Higher threshold for systematic reviews
screener = CompensationPaperScreener(quality_threshold=50.0)

# Lower threshold for exploratory research
screener = CompensationPaperScreener(quality_threshold=30.0)
```

### **Focusing on Specific Areas**

```python
# Hip compensation focus
config = {
    "focus_regions": ["hip"],
    "preferred_journals": ["Physical Therapy", "JOSPT"],
    "compensation_types": ["substitution", "weakness"]
}

screener = CompensationPaperScreener(config=config)
```

### **Search Parameters**

```python
# Search more papers initially (broader net)
papers = screener.screen_papers(limit=50)

# Search fewer papers (quick overview)
papers = screener.screen_papers(limit=10)
```

## 🔬 Advanced Features

### **Detailed Analysis**

```python
# Get detailed scoring breakdown
for paper in papers:
    details = screener.get_scoring_details(paper['paper_id'])

    print(f"Field Score Components:")
    print(f"  Journal Impact: {details['journal_score']}")
    print(f"  Keywords: {details['keyword_score']}")
    print(f"  Anatomical: {details['anatomy_score']}")

    print(f"Quality Score Components:")
    print(f"  Study Design: {details['design_score']}")
    print(f"  Sample Size: {details['sample_score']}")
    print(f"  Citations: {details['citation_score']}")
```

### **Filtering and Sorting**

```python
# Filter by specific criteria
high_quality = [p for p in papers if p['total_score'] >= 60]
recent_papers = [p for p in papers if p['year'] >= 2020]
rct_studies = [p for p in papers if 'RCT' in p['study_design']]

# Sort by different criteria
papers_by_score = sorted(papers, key=lambda x: x['total_score'], reverse=True)
papers_by_year = sorted(papers, key=lambda x: x['year'], reverse=True)
```

### **Export Results**

```python
# Export to different formats
screener.export_results(papers, format='csv', filename='screened_papers.csv')
screener.export_results(papers, format='json', filename='papers.json')
screener.export_citation_list(papers, style='apa', filename='citations.txt')
```

## 📈 Understanding Paper Metadata

### **Compensation Indicators**

Each paper includes automatically extracted compensation information:

```python
paper['compensation_indicators'] = {
    "primary_region": "hip",                    # Main anatomical focus
    "dysfunction_type": "weakness",             # Type of dysfunction
    "compensation_mechanism": "substitution",   # How compensation occurs
    "assessment_methods": ["EMG", "3D_motion"], # Methods used
    "treatment_approaches": ["strengthening"]   # Interventions studied
}
```

### **Clinical Relevance**

```python
paper['clinical_relevance'] = {
    "condition": "hip_abductor_weakness",       # Specific condition
    "population": "athletes",                   # Study population
    "outcome_measures": ["strength", "pain"],  # Outcomes measured
    "treatment_duration": "8_weeks"            # Intervention length
}
```

## 🎓 Best Practices

### **For Clinical Practice**

1. **Start with High-Quality Papers (≥60 points)**
   - Use for evidence-based protocols
   - Reference in clinical decision-making
   - Share with colleagues and patients

2. **Review Multiple Related Papers**
   - Look for consistency across studies
   - Note conflicting findings
   - Consider population differences

3. **Check Assessment Methods**
   - Ensure methods are feasible in your setting
   - Consider equipment and training needs
   - Validate with your patient population

### **For Research**

1. **Use Detailed Scoring Information**
   - Document selection criteria
   - Report screening statistics
   - Justify inclusion/exclusion decisions

2. **Save Search Parameters**
   - Record configuration settings
   - Document date ranges
   - Note database sources

3. **Track Updates**
   - Re-run searches periodically
   - Monitor new high-quality papers
   - Update systematic reviews

### **For Education**

1. **Use Score Distribution for Teaching**
   - Show students how to evaluate quality
   - Demonstrate critical appraisal skills
   - Compare different study designs

2. **Create Learning Cases**
   - Select papers with clear patterns
   - Use for case-based learning
   - Develop clinical reasoning skills

## 🚨 Common Issues and Solutions

### **Low Paper Yield**

**Problem:** Getting fewer papers than expected

**Solutions:**
- Lower quality threshold temporarily
- Expand search terms
- Include older papers (extend date range)
- Check if search terms are too specific

### **Poor Quality Results**

**Problem:** Papers don't seem clinically relevant

**Solutions:**
- Increase quality threshold
- Add specific journals to focus list
- Exclude certain article types
- Refine compensation keywords

### **Inconsistent Results**

**Problem:** Getting different papers on repeat searches

**Solutions:**
- Database updates affect results
- Some papers may be near threshold
- Check for API rate limiting
- Verify search parameter consistency

### **Technical Errors**

**Problem:** API errors or timeouts

**Solutions:**
- Check internet connection
- Verify API keys are valid
- Reduce batch size for processing
- Implement retry mechanisms

## 📋 Troubleshooting Checklist

**Before Starting:**
- [ ] Verify API keys are configured
- [ ] Check internet connectivity
- [ ] Confirm Python dependencies installed
- [ ] Review configuration settings

**During Screening:**
- [ ] Monitor progress indicators
- [ ] Check for error messages
- [ ] Verify results make sense
- [ ] Save intermediate results

**After Screening:**
- [ ] Review score distributions
- [ ] Validate top papers manually
- [ ] Export results for backup
- [ ] Document search parameters

## 📞 Getting Help

### **Documentation Resources**
- **[API Reference](../api/paper-screener.md)** - Technical documentation
- **[Paper Screening Demo](../examples/paper-screening-demo.md)** - Interactive example
- **[Quality Standards](../research/quality-standards.md)** - Detailed scoring criteria

### **Common Questions**

**Q: How often should I run new searches?**
A: For clinical practice, monthly searches are usually sufficient. For active research, weekly searches may be needed.

**Q: Can I modify the scoring criteria?**
A: Yes, quality thresholds and focus areas can be customized. Contact support for advanced customization.

**Q: What if I disagree with a paper's score?**
A: The system is designed for high-volume screening. Manual review of borderline cases is always recommended.

**Q: How do I cite the screening results?**
A: Include the screening methodology, parameters used, and date of search in your methods section.

## 🔗 Next Steps

After screening papers, you can:

1. **Proceed to 5WHY Analysis**
   - Analyze selected papers for causal relationships
   - Extract compensation patterns
   - Identify treatment implications

2. **Build Knowledge Graphs**
   - Connect related concepts
   - Visualize relationships
   - Identify research gaps

3. **Create Obsidian Vaults**
   - Organize papers in structured format
   - Generate cross-linked documentation
   - Support clinical decision-making

---

**📋 This guide provides everything you need to effectively use the paper screening system for finding high-quality compensation research relevant to your clinical or research needs.**