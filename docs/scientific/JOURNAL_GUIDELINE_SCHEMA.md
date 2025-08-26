# JournalGuideline Node Schema

## Properties
- journal: string (unique)
- word_counts: object {abstract:int?, main:int?, methods:int|string?, refs:int?}
- refs_style: enum
- figures_limits: object {max:int?, panels:string?}
- tables_limits: object {max:int?}
- image_specs: object {dpi:int?, width_mm:int?, height_mm:int?, formats:[string]}
- supplement_rules: [string]
- sections: [string]
- source_url: string
- source_hash: string
- retrieved_at: ISO datetime
- publisher: string

## Versioning (optional)
- create GuidelineVersion nodes and link via HAS_VERSION