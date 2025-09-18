# 🔌 API Reference

> **Complete API documentation for the Compensation Research System**

## 🚀 API Overview

The Compensation Research System provides a comprehensive REST API for programmatic access to research data, analysis results, and system functionality.

### **Base URLs**
```
Production:  https://api.compensation-research.com/v1
Staging:     https://staging-api.compensation-research.com/v1
Local:       http://localhost:8080/api/v1
```

### **Authentication**
```http
# API Key Authentication (recommended)
Authorization: Bearer your_api_key_here

# Basic Authentication (development only)
Authorization: Basic base64(username:password)
```

## 📚 Core APIs

### **[Paper Screening API](paper-screener.md)**
Intelligent academic paper filtering and quality assessment
```
GET    /papers/screen           # Screen new papers
POST   /papers/bulk-screen      # Bulk screening operation
GET    /papers/quality-metrics  # Quality assessment data
```

### **[5WHY Analysis API](why-analyzer.md)**
Causal analysis using 5WHY methodology
```
POST   /analysis/5why           # Perform 5WHY analysis
GET    /analysis/5why/{id}      # Retrieve analysis results
GET    /analysis/patterns       # Get compensation patterns
```

### **[Node Connection API](node-connector.md)**
Knowledge graph construction and relationship mapping
```
GET    /nodes                   # List all nodes
POST   /nodes/connect           # Create node connections
GET    /nodes/{id}/relationships # Get node relationships
GET    /graph/export            # Export knowledge graph
```

### **[Obsidian Vault API](obsidian-generator.md)**
Wiki generation and content management
```
GET    /vault/structure         # Get vault organization
POST   /vault/generate          # Generate vault content
GET    /vault/download          # Download complete vault
GET    /vault/stats             # Vault statistics
```

## 🔍 Quick Start Examples

### **Screen Papers**
```python
import requests

# Screen latest compensation papers
response = requests.get(
    "https://api.compensation-research.com/v1/papers/screen",
    headers={"Authorization": "Bearer your_api_key"},
    params={
        "limit": 10,
        "quality_threshold": 8.0,
        "focus_area": "hip_compensation"
    }
)

papers = response.json()
print(f"Found {len(papers['results'])} papers")
```

### **Perform 5WHY Analysis**
```python
# Analyze a specific paper
analysis_request = {
    "paper_id": "openalex:W1234567890",
    "methodology": "compensation_focus",
    "depth": 5
}

response = requests.post(
    "https://api.compensation-research.com/v1/analysis/5why",
    headers={"Authorization": "Bearer your_api_key"},
    json=analysis_request
)

analysis = response.json()
print(f"Analysis completed with {len(analysis['why_levels'])} levels")
```

### **Query Knowledge Graph**
```python
# Get nodes related to gluteus medius
response = requests.get(
    "https://api.compensation-research.com/v1/nodes",
    headers={"Authorization": "Bearer your_api_key"},
    params={
        "search": "gluteus medius",
        "type": "muscle",
        "include_connections": True
    }
)

nodes = response.json()
print(f"Found {len(nodes['results'])} related nodes")
```

### **Generate Vault Content**
```python
# Generate custom vault section
vault_request = {
    "focus_area": "knee_compensation",
    "include_patterns": True,
    "format": "obsidian_markdown",
    "depth": "comprehensive"
}

response = requests.post(
    "https://api.compensation-research.com/v1/vault/generate",
    headers={"Authorization": "Bearer your_api_key"},
    json=vault_request
)

vault_data = response.json()
print(f"Generated {vault_data['file_count']} vault files")
```

## 📊 Data Models

### **Paper Object**
```json
{
  "id": "openalex:W1234567890",
  "title": "Gluteus medius weakness and hip compensation",
  "authors": ["Author Name"],
  "journal": "Journal of Biomechanics",
  "year": 2023,
  "doi": "10.1016/j.jbiomech.2023.example",
  "quality_scores": {
    "overall": 8.5,
    "methodology": 9.0,
    "relevance": 8.0,
    "impact": 8.5
  },
  "compensation_focus": {
    "primary_area": "hip",
    "mechanisms": ["weakness", "substitution"],
    "confidence": 0.92
  },
  "abstract": "Research abstract text...",
  "keywords": ["compensation", "gluteus medius", "biomechanics"],
  "created_at": "2023-09-18T10:30:00Z",
  "updated_at": "2023-09-18T10:30:00Z"
}
```

### **5WHY Analysis Object**
```json
{
  "id": "5why_analysis_uuid",
  "paper_id": "openalex:W1234567890",
  "why_levels": [
    {
      "level": 1,
      "question": "Why does hip pain occur during running?",
      "answer": "Gluteus medius weakness causes hip instability",
      "evidence": "EMG studies show 40% reduction in activation",
      "confidence": 0.88
    }
  ],
  "compensation_pattern": {
    "name": "Hip Abductor Weakness Pattern",
    "primary_dysfunction": "Gluteus medius weakness",
    "compensatory_strategy": "TFL overactivity",
    "mechanism_type": "substitution"
  },
  "clinical_significance": "High - common in runners",
  "treatment_recommendations": [
    "Progressive hip abductor strengthening",
    "TFL stretching and release techniques"
  ],
  "created_at": "2023-09-18T10:35:00Z"
}
```

### **Node Object**
```json
{
  "id": "node_uuid",
  "type": "muscle",
  "name": "Gluteus Medius",
  "attributes": {
    "primary_function": "Hip abduction and stabilization",
    "common_dysfunctions": ["weakness", "inhibition"],
    "compensation_patterns": ["TFL substitution", "hip hiking"]
  },
  "connections": [
    {
      "target_node": "TFL_node_uuid",
      "relationship_type": "compensatory_substitution",
      "strength": 0.85,
      "evidence_count": 12
    }
  ],
  "metadata": {
    "paper_count": 45,
    "clinical_frequency": "very_common",
    "last_updated": "2023-09-18T10:40:00Z"
  }
}
```

## 🔧 API Features

### **Filtering & Search**
```http
# Advanced filtering
GET /papers/screen?journal=Physical+Therapy&year_from=2020&quality_min=7.0

# Full-text search
GET /nodes?search=gluteus+medius+weakness&type=muscle,pattern

# Faceted search
GET /analysis/5why?compensation_type=substitution&body_region=hip
```

### **Pagination**
```json
{
  "results": [...],
  "pagination": {
    "page": 1,
    "per_page": 25,
    "total_items": 1250,
    "total_pages": 50,
    "has_next": true,
    "has_prev": false
  }
}
```

### **Sorting**
```http
# Sort by quality score (descending)
GET /papers/screen?sort=-quality_score

# Sort by publication date (ascending)
GET /papers/screen?sort=publication_date

# Multiple sort criteria
GET /papers/screen?sort=-quality_score,publication_date
```

### **Field Selection**
```http
# Select specific fields only
GET /papers/screen?fields=id,title,quality_scores,compensation_focus

# Include related data
GET /nodes?include=connections,metadata
```

## 🚨 Error Handling

### **Error Response Format**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid quality threshold value",
    "details": {
      "field": "quality_threshold",
      "value": "invalid_value",
      "expected": "Number between 0.0 and 10.0"
    },
    "timestamp": "2023-09-18T10:45:00Z",
    "request_id": "req_uuid"
  }
}
```

### **Common Error Codes**
```yaml
400 BAD_REQUEST:
  - VALIDATION_ERROR: Invalid input parameters
  - MISSING_FIELD: Required field not provided

401 UNAUTHORIZED:
  - INVALID_API_KEY: API key is invalid or expired
  - MISSING_AUTH: No authentication provided

403 FORBIDDEN:
  - INSUFFICIENT_PERMISSIONS: API key lacks required permissions
  - RATE_LIMIT_EXCEEDED: Too many requests

404 NOT_FOUND:
  - RESOURCE_NOT_FOUND: Requested resource doesn't exist
  - ENDPOINT_NOT_FOUND: Invalid API endpoint

429 TOO_MANY_REQUESTS:
  - RATE_LIMIT: Request rate exceeded

500 INTERNAL_SERVER_ERROR:
  - PROCESSING_ERROR: Internal processing failure
  - DATABASE_ERROR: Database connection issues
```

## 📈 Rate Limiting

### **Default Limits**
```yaml
Free Tier:
  - 100 requests per hour
  - 1000 requests per day
  - No burst allowance

Pro Tier:
  - 1000 requests per hour
  - 10000 requests per day
  - 50 request burst

Enterprise:
  - Custom limits
  - Priority processing
  - Dedicated support
```

### **Rate Limit Headers**
```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1632847200
X-RateLimit-Burst: 50
```

## 🔐 Security

### **API Key Management**
```bash
# Generate new API key
curl -X POST https://api.compensation-research.com/v1/auth/keys \
  -H "Authorization: Bearer master_key" \
  -d '{"name": "Research Integration", "permissions": ["read", "write"]}'

# Revoke API key
curl -X DELETE https://api.compensation-research.com/v1/auth/keys/key_id \
  -H "Authorization: Bearer master_key"
```

### **Webhook Security**
```python
import hmac
import hashlib

def verify_webhook(payload, signature, secret):
    expected = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

## 📞 Support

### **API Status**
- **Status Page**: https://status.compensation-research.com
- **Uptime Target**: 99.9%
- **Response Time**: < 200ms (95th percentile)

### **Getting Help**
- **Documentation**: Each endpoint has detailed docs with examples
- **Support Email**: api-support@compensation-research.com
- **GitHub Issues**: Technical problems and feature requests
- **Stack Overflow**: Tag questions with `compensation-research-api`

---

**🚀 Ready to integrate? Start with our [Quick Start Guide](../installation.md) or explore specific API endpoints above.**