---
source_url: https://www.itnb.ch/en/terms/service-level-agreement
title: itnb
crawled_at: 2025-12-25 02:54:34
---

# itnb

[![itnb](https://www.itnb.ch/img/02_itnb_logo_BLUE_Blue_slogan_ORG_1_ea8d52891c.png?q=eyJyZXNpemUiOnsidyI6NzUwLCJmaWxsIjoiY292ZXIifX0=) header.backToHome](https://www.itnb.ch/en)
  * Products and Services
  * Solutions
  * Ecosystem
  * Company


English
[Contact](https://www.itnb.ch/en/company/about-itnb/contact)[Portal](https://console.itnb.ch/)
## Service Level Agreement
### Preamble and Relationship to Terms of Service and DPA
This Service Level Agreement ("SLA") forms part of and is governed by the Phoenix Terms of Service ("ToS") and the Data Processing Agreement ("DPA"). It describes the service availability commitments, support response times, and remedies available to Customers. Capitalised terms not defined here have the meanings set out in the ToS or DPA. In case of conflict, the order of precedence applies: (1) Order Form/SOW, (2) DPA (for data protection), (3) SLA (for availability and support), (4) ToS.
### 1. Scope of Services Covered
This SLA applies to Phoenix-provided Infrastructure-as-a-Service (IaaS), Platform-as-a-Service (PaaS), and Software-as-a-Service (SaaS) offerings, including Phoenix-hosted AI models and the AI Concierge application. For third-party or open-source models, plugins, or integrations, Phoenix is not responsible for their availability, as set out in the ToS (Section 1.6).
### 2. Service Availability
2.1 Infrastructure (IaaS). Phoenix commits to a minimum Monthly Uptime Percentage of 99.99% for core infrastructure services (compute, storage, networking, GPUs), measured on a 24x7x365 basis, excluding scheduled maintenance agreed in advance.
2.2 Platform & SaaS. Phoenix commits to a minimum Monthly Uptime Percentage of 98% for Phoenix-hosted SaaS applications (e.g., AI Concierge) and Model-as-a-Service offerings, during standard business hours (Monday–Friday, 08:00–17:00 CET, excluding Swiss public holidays). Scheduled maintenance is excluded.
2.3 Scheduled Maintenance. Phoenix will provide at least 48 hours’ notice of scheduled maintenance. Maintenance windows will, where possible, be scheduled outside of core business hours. Emergency maintenance may be conducted without notice where necessary for security or stability.
2.4 Exclusions. Availability commitments do not apply to: (a) downtime caused by Customer misuse or unauthorised actions; (b) downtime caused by third-party applications, integrations, or providers not under Phoenix’s control; (c) beta/preview features; (d) force majeure events as defined in the ToS.
### 3. Measurement and Reporting
Availability is measured monthly using Phoenix’s monitoring systems, which track service uptime at the infrastructure and application layers. Phoenix may make summary availability reports available upon request or via the customer portal.
### 4. Support Commitments
Phoenix provides tiered support with response times based on severity, as set out below. Resolution times are targets, not guarantees.
Severity Level | Definition | Initial Response Time (Plan Dependent)  
---|---|---  
Severity 1 – Critical | Production service unavailable or severely degraded with no workaround. | Within 1 hour (24x7)  
Severity 2 – High | Significant functionality impaired; workaround available. | Within 4 business hours  
Severity 3 – Medium | Non-critical issue; partial degradation; workaround available. | Within 1 business day  
Severity 4 – Low | General questions, cosmetic issues, feature requests. | Within 2 business days  
### 5. Remedies for Failure to Meet SLA
If Phoenix fails to meet an availability commitment under Section 2, Customer may be eligible for a Service Credit. Service Credits are the sole and exclusive remedy for failure to meet SLA commitments.
5.1 Service Credit Calculation. Service Credits are calculated as a percentage of the monthly fee for the affected Service, based on the Monthly Uptime Percentage, as follows:
Monthly Uptime Percentage | Service Credit  
---|---  
<99.99% (IaaS only) | 5% of monthly fee for affected service  
<98.0% (SaaS/PaaS) | 10% of monthly fee for affected service  
<95.0% (any service) | 25% of monthly fee for affected service  
<90.0% (any service) | 50% of monthly fee for affected service  
5.2 Claim Procedure. To receive a Service Credit, Customer must submit a claim to support@phoenix-technologies.ch within thirty (30) days of the incident, including the dates/times of unavailability. Claims will be validated against Phoenix’s records.
5.3 Limitations. Service Credits may not exceed 50% of the monthly fees for the affected Service. Credits are applied to future invoices and are non-refundable. SLA remedies do not apply to trial, beta, or preview Services.
### 6. Miscellaneous
This SLA does not modify the disclaimers, exclusions, or limitations of liability set forth in the ToS. All capitalised terms and obligations in the ToS (including force majeure, suspension rights, and exclusions) apply equally to this SLA. Phoenix may update this SLA from time to time, with notice provided to Customers via the portal or email.
### 7. Support Plans and Response Times
Phoenix offers three tiers of support services: Basic, Advanced, and Premium. These plans provide different levels of coverage, response times, and service features. Customers select a support plan in their Order Form, which governs the level of support provided.
7.1 Support Plan Summaries
• Basic Support: Provides essential coverage, including access to the support portal, email assistance, and response within extended business hours. Suitable for non-critical workloads or evaluation purposes.
• Advanced Support: Adds faster response times, access via Teams, and higher priority ticket handling. Recommended for production workloads requiring timely support and periodic assistance.
• Premium Support: Provides the highest level of responsiveness, 24x7 availability, rapid response commitments, proactive monitoring, and access to a Technical Account Manager. Designed for mission-critical enterprise deployments requiring guaranteed coverage.
7.2 Response Time Commitments
The table below consolidates Phoenix’s commitments (based on internal SLA and aligned with TogetherAI-style practices). It includes Initial Response Time (IRT), Ticket Qualification (QT), and Update Frequency Time (UFT).
Severity  
Level | Description | Basic | Advanced | Premium  
---|---|---|---|---  
Severity 1 – Critical | Outage impacting entire customer population | IRT: 24h | QT: +24h | UFT: +24h | IRT: 1h | QT: +8h | UFT: +8h | IRT: 30m | QT: +4h | UFT: +4h  
Severity 2 – High | Significant functionality impaired; workaround available | IRT: 48h | QT: +48h | UFT: +48h | IRT: 4h | QT: +12h | UFT: +30h | IRT: 2h | QT: +7h | UFT: +20h  
Severity 3 – Medium | Minor functionality issues, not business critical | IRT: 96h | IRT: 72h | IRT: 48h  
Severity 4 – Low | General questions, cosmetic issues, documentation requests | IRT: 144h | IRT: 120h | IRT: 96h  
7.3 Feature Comparison by Plan
Beyond response times, each plan includes additional features as summarized below.
Feature | Basic | Advanced | Premium  
---|---|---|---  
Communication Channels | Support Platform | Support Platform, Teams | Support Platform, Teams, Email  
Training / Services (1-year commit) | No | No | 20 hours total  
Priority Queueing | No | No | Yes  
Technical Account Manager | No | No | Yes  
API Credits | Standard SLA | Standard SLA | Standard SLA  
Proactive Monitoring & Escalation  | No | No | Yes  
Customer Reporting Tools (uptime dashboards, SLA reports) | Yes | Yes | Yes  
Dedicated Support Engineer1 | No | No | Yes  
Global Coverage (24x7)1 | No | No | Yes  
[1] Enterprise accounts only
## Safe,  
Secure,  
Swiss.
[Contact](https://www.itnb.ch/en/company/about-itnb/contact)[Portal](https://console.itnb.ch/)[LinkedinOpen Linkedin profile](https://www.linkedin.com/company/itnb-ag/)
  * ### Products and Services
    * ### Infrastructure as a Service
      * [Sovereign Cloud](https://www.itnb.ch/en/products-and-services/infrastructure-as-a-service/sovereign-cloud)
      * [Speedboat](https://www.itnb.ch/en/products-and-services/infrastructure-as-a-service/speedboat)
      * [GPU as a Service](https://www.itnb.ch/en/products-and-services/infrastructure-as-a-service/gpu-as-a-service)
    * ### Platform as a Service
      * [AI Model as a Service](https://www.itnb.ch/en/products-and-services/platform-as-a-service/ai-model-as-a-service)
    * ### Software as a Service
      * [Sovereign Orchestrator](https://www.itnb.ch/en/products-and-services/software-as-a-service/sovereign-orchestrator)
    * ### Professional Services
      * [NorthStar AI Accelerator](https://www.itnb.ch/en/products-and-services/professional-services/northstar-ai-accelerator)
      * [Project Management](https://www.itnb.ch/en/products-and-services/professional-services/project-management)
    * ### Cybersecurity
      * [Security Operations Center as a Service](https://www.itnb.ch/en/products-and-services/cybersecurity/security-operations-center-as-a-service)
      * [Sovereign Endpoint Security (EDR)](https://www.itnb.ch/en/products-and-services/cybersecurity/sovereign-endpoint-security)
  * ### Solutions
    * ### Industries
      * [Healthcare and Life Sciences](https://www.itnb.ch/en/solutions/industries/healthcare-and-life-sciences)
      * [Education and Research](https://www.itnb.ch/en/solutions/industries/education-and-research)
      * [Financial Services](https://www.itnb.ch/en/solutions/industries/financial-services)
      * [Media](https://www.itnb.ch/en/solutions/industries/media)
    * ### Use Cases
      * [Run AI Workloads](https://www.itnb.ch/en/solutions/use-cases/run-ai-workloads)
      * [Data Center Exit](https://www.itnb.ch/en/solutions/use-cases/data-center-exit)
      * [Run Critical Applications](https://www.itnb.ch/en/solutions/use-cases/run-critical-applications)
      * [Reduce CO2 Emissions](https://www.itnb.ch/en/solutions/use-cases/reduce-co2-emissions)
  * ### Ecosystem
    * [Partner Network](https://www.itnb.ch/en/ecosystem/partner-network)
      * [Success Stories](https://www.itnb.ch/en/ecosystem/partner-network/success-stories)
      * [AI Innovation Center](https://www.itnb.ch/en/ecosystem/partner-network/ai-innovation-center)
  * ### Company
    * [About ITNB](https://www.itnb.ch/en/company/about-itnb)
      * [Contact](https://www.itnb.ch/en/company/about-itnb/contact)


[![PHOENIX-SYSTEMS](https://www.itnb.ch/img/02_itnb_logo_BLUE_Blue_slogan_ORG_1_ea8d52891c.png?q=eyJyZXNpemUiOnsidyI6OTYsImZpbGwiOiJjb3ZlciJ9fQ==)](https://www.itnb.ch/en)
Copyright © 2025 ITNB
  * English
  * [Terms](https://www.itnb.ch/en/terms)
  * [Privacy Policy](https://www.itnb.ch/en/privacy-policy)
  * [Imprint](https://www.itnb.ch/en/imprint)
  * [Documentation](https://documentation.kvant.cloud)
  * [Status](https://status.kvant.cloud/)


