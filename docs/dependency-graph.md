# fraq — Dependency Graph

> 70 modules, 197 dependency edges

## Module Dependencies

```mermaid
graph LR
    training_data --> fraq
    applications --> fraq
    async_streaming --> fraq
    async_streaming --> streaming
    query_examples --> fraq
    sqlite_examples --> fraq
    pipeline_examples --> fraq
    api_server --> fraq
    api_server --> streaming
    api_server --> text2fraq
    main --> fraq
    main --> formats
    main --> generators
    main --> fraq
    main --> generators
    main --> fraq
    main --> generators
    sensor_examples --> fraq
    network_web_examples --> fraq
    new_features_demo --> fraq
    new_features_demo --> benchmarks
    new_features_demo --> dataframes
    new_features_demo --> ifs
    new_features_demo --> inference
    sse_examples --> fraq
    nlp2cmd_integration --> fraq
    text2fraq_examples --> fraq
    text2fraq_files --> fraq
    new_features --> fraq
    new_features --> text2fraq
    new_features --> parser_llm
    main --> fraq
    main --> generators
    fraq --> adapters
    fraq --> api
    fraq --> core
    fraq --> formats
    fraq --> generators
    fraq --> ifs
    fraq --> query
    fraq --> schema_export
    fraq --> text2fraq
    fraq --> types
    adapters --> fraq
    adapters --> base
    adapters --> file_adapter
    adapters --> file_search
    adapters --> http_adapter
    adapters --> hybrid_adapter
    adapters --> registry
    adapters --> sensor_adapter
    adapters --> sql_adapter
    base --> fraq
    base --> core
    base --> query
    file_adapter --> fraq
    file_adapter --> adapters
    file_adapter --> base
    file_adapter --> core
    file_adapter --> formats
    file_adapter --> query
    file_search --> fraq
    file_search --> adapters
    file_search --> base
    file_search --> core
    file_search --> formats
    file_search --> query
    http_adapter --> fraq
    http_adapter --> adapters
    http_adapter --> base
    http_adapter --> file_adapter
    http_adapter --> core
    http_adapter --> formats
    http_adapter --> query
    hybrid_adapter --> fraq
    hybrid_adapter --> adapters
    hybrid_adapter --> base
    hybrid_adapter --> core
    hybrid_adapter --> query
    registry --> fraq
    registry --> adapters
    registry --> base
    registry --> file_adapter
    registry --> http_adapter
    registry --> hybrid_adapter
    registry --> sensor_adapter
    registry --> sql_adapter
    registry --> query
    sensor_adapter --> fraq
    sensor_adapter --> adapters
    sensor_adapter --> base
    sensor_adapter --> core
    sensor_adapter --> formats
    sensor_adapter --> generators
    sensor_adapter --> query
    sql_adapter --> fraq
    sql_adapter --> adapters
    sql_adapter --> base
    sql_adapter --> core
    sql_adapter --> query
    api --> fraq
    api --> core
    api --> providers
    api --> faker_provider
    benchmarks --> fraq
    benchmarks --> ifs
    benchmarks --> inference
    cli --> fraq
    cli --> adapters
    cli --> core
    cli --> formats
    cli --> generators
    cli --> text2fraq
    dataframes --> fraq
    formats --> fraq
    formats --> binary
    formats --> prepare
    formats --> registry
    formats --> text
    binary --> fraq
    binary --> formats
    binary --> prepare
    prepare --> fraq
    prepare --> core
    text --> fraq
    text --> formats
    text --> prepare
    generators --> fraq
    generators --> core
    inference --> fraq
    inference --> ifs
    providers --> fraq
    providers --> faker_provider
    query --> fraq
    query --> core
    query --> formats
    schema_export --> fraq
    schema_export --> core
    server --> fraq
    server --> adapters
    server --> file_search
    server --> core
    server --> generators
    server --> text2fraq
    server --> router
    server --> session
    streaming --> fraq
    streaming --> core
    streaming --> query
    text2fraq --> fraq
    text2fraq --> config
    text2fraq --> file_search_parser
    text2fraq --> llm_client
    text2fraq --> models
    text2fraq --> parser_llm
    text2fraq --> parser_rules
    text2fraq --> session
    text2fraq --> shortcuts
    file_search_parser --> fraq
    file_search_parser --> adapters
    file_search_parser --> file_search
    file_search_parser --> formats
    llm_client --> fraq
    llm_client --> text2fraq
    llm_client --> config
    llm_client --> models
    models --> fraq
    models --> query
    parser_llm --> fraq
    parser_llm --> core
    parser_llm --> query
    parser_llm --> text2fraq
    parser_llm --> config
    parser_llm --> llm_client
    parser_llm --> models
    parser_llm --> parser_rules
    parser_rules --> fraq
    parser_rules --> core
    parser_rules --> query
    parser_rules --> text2fraq
    parser_rules --> models
    session --> fraq
    session --> text2fraq
    session --> config
    session --> models
    session --> parser_llm
    session --> parser_rules
    shortcuts --> fraq
    shortcuts --> core
    shortcuts --> text2fraq
    shortcuts --> config
    shortcuts --> file_search_parser
    shortcuts --> models
    shortcuts --> parser_llm
    shortcuts --> parser_rules
    main_websocket --> fraq
    main_websocket --> generators
```

## Coupling Matrix

| | training_data | bash_examples | app_integrations | applications | async_streaming | query_examples | bash_examples | run | sqlite_examples | pipeline_examples | api_server | main | run | main | app | run | main | sensor_examples | network_web_examples | new_features_demo | nlp_examples | sse_examples | nlp2cmd_integration | text2fraq_examples | text2fraq_files | new_features | main | run | fraq | adapters | base | file_adapter | file_search | http_adapter | hybrid_adapter | registry | sensor_adapter | sql_adapter | api | benchmarks | cli | core | dataframes | formats | binary | prepare | registry | text | generators | ifs | inference | providers | faker_provider | query | schema_export | server | streaming | text2fraq | config | file_search_parser | llm_client | models | parser_llm | parser_rules | router | session | shortcuts | types | main_websocket | project |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **training_data** | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **bash_examples** |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **app_integrations** |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **applications** |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **async_streaming** |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **query_examples** |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **bash_examples** |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **run** |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **sqlite_examples** |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **pipeline_examples** |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **api_server** |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  |  |  |  |  |  |  |  |  |  |  |  |
| **main** |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **run** |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **main** |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **app** |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **run** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **main** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **sensor_examples** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **network_web_examples** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **new_features_demo** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  | → |  |  | → |  |  |  |  |  |  | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **nlp_examples** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **sse_examples** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **nlp2cmd_integration** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **text2fraq_examples** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **text2fraq_files** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **new_features** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  | → |  |  |  |  |  |  |  |
| **main** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **run** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **fraq** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · | → |  |  |  |  |  |  |  |  | → |  |  | → |  | → |  |  |  |  | → | → |  |  |  | → | → |  |  | → |  |  |  |  |  |  |  |  |  | → |  |  |
| **adapters** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | · | → | → | → | → | → | → | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **base** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  | · |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **file_adapter** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → | · |  |  |  |  |  |  |  |  |  | → |  | → |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **file_search** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → |  | · |  |  |  |  |  |  |  |  | → |  | → |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **http_adapter** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → | → |  | · |  |  |  |  |  |  |  | → |  | → |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **hybrid_adapter** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → |  |  |  | · |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **registry** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → | → |  | → | → | · | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **sensor_adapter** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → |  |  |  |  |  | · |  |  |  |  | → |  | → |  |  |  |  | → |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **sql_adapter** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → |  |  |  |  |  |  | · |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **api** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  | · |  |  | → |  |  |  |  |  |  |  |  |  | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **benchmarks** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **cli** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  |  |  |  |  |  |  |  |  |  | · | → |  | → |  |  |  |  | → |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |
| **core** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **dataframes** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **formats** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · | → | → | → | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **binary** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | · | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **prepare** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **registry** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **text** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  | → |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **generators** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **ifs** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **inference** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **providers** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **faker_provider** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **query** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  | → |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **schema_export** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **server** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  |  | → |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  | → |  |  |  |  |  |  | · |  | → |  |  |  |  |  |  | → | → |  |  |  |  |
| **streaming** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  | · |  |  |  |  |  |  |  |  |  |  |  |  |  |
| **text2fraq** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · | → | → | → | → | → | → |  | → | → |  |  |  |
| **config** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |  |
| **file_search_parser** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  |  | → |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |  |  |
| **llm_client** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  | · | → |  |  |  |  |  |  |  |  |
| **models** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  | · |  |  |  |  |  |  |  |  |
| **parser_llm** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  | → | → |  | → | → | · | → |  |  |  |  |  |  |
| **parser_rules** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  | → |  |  |  | → |  | · |  |  |  |  |  |  |
| **router** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |  |  |  |
| **session** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → |  |  | → | → | → |  | · |  |  |  |  |
| **shortcuts** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → | → | → |  | → | → | → |  |  | · |  |  |  |
| **types** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |  |
| **main_websocket** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | → |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |  |
| **project** |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | · |

## Fan-in / Fan-out

| Module | Fan-in | Fan-out |
|--------|--------|---------|
| `examples.ai_ml.training_data` | 0 | 1 |
| `examples.bash_examples` | 0 | 0 |
| `examples.basic.app_integrations` | 0 | 0 |
| `examples.basic.applications` | 0 | 1 |
| `examples.basic.async_streaming` | 0 | 2 |
| `examples.basic.query_examples` | 0 | 1 |
| `examples.cli-docker.bash_examples` | 0 | 0 |
| `examples.cli-docker.run` | 0 | 0 |
| `examples.database.sqlite_examples` | 0 | 1 |
| `examples.etl.pipeline_examples` | 0 | 1 |
| `examples.fastapi-docker.api_server` | 0 | 3 |
| `examples.fastapi-docker.main` | 0 | 3 |
| `examples.fastapi-docker.run` | 0 | 0 |
| `examples.fullstack-docker.api.main` | 0 | 2 |
| `examples.fullstack-docker.frontend.app` | 0 | 0 |
| `examples.fullstack-docker.run` | 0 | 0 |
| `examples.fullstack-docker.websocket.main` | 0 | 2 |
| `examples.iot.sensor_examples` | 0 | 1 |
| `examples.network.network_web_examples` | 0 | 1 |
| `examples.new_features_demo` | 0 | 5 |
| `examples.nlp_examples` | 0 | 0 |
| `examples.streaming.sse_examples` | 0 | 1 |
| `examples.text2fraq.nlp2cmd_integration` | 0 | 1 |
| `examples.text2fraq.text2fraq_examples` | 0 | 1 |
| `examples.text2fraq.text2fraq_files` | 0 | 1 |
| `examples.v028.new_features` | 0 | 3 |
| `examples.websocket-docker.main` | 0 | 2 |
| `examples.websocket-docker.run` | 0 | 0 |
| `fraq` | 52 | 10 |
| `fraq.adapters` | 11 | 9 |
| `fraq.adapters.base` | 8 | 3 |
| `fraq.adapters.file_adapter` | 3 | 6 |
| `fraq.adapters.file_search` | 3 | 6 |
| `fraq.adapters.http_adapter` | 2 | 7 |
| `fraq.adapters.hybrid_adapter` | 2 | 5 |
| `fraq.adapters.registry` | 1 | 9 |
| `fraq.adapters.sensor_adapter` | 2 | 7 |
| `fraq.adapters.sql_adapter` | 2 | 5 |
| `fraq.api` | 1 | 4 |
| `fraq.benchmarks` | 1 | 3 |
| `fraq.cli` | 0 | 6 |
| `fraq.core` | 19 | 0 |
| `fraq.dataframes` | 1 | 1 |
| `fraq.formats` | 11 | 5 |
| `fraq.formats.binary` | 1 | 3 |
| `fraq.formats.prepare` | 3 | 2 |
| `fraq.formats.registry` | 1 | 0 |
| `fraq.formats.text` | 1 | 3 |
| `fraq.generators` | 9 | 2 |
| `fraq.ifs` | 4 | 0 |
| `fraq.inference` | 2 | 2 |
| `fraq.providers` | 1 | 2 |
| `fraq.providers.faker_provider` | 2 | 0 |
| `fraq.query` | 13 | 3 |
| `fraq.schema_export` | 1 | 2 |
| `fraq.server` | 0 | 8 |
| `fraq.streaming` | 2 | 3 |
| `fraq.text2fraq` | 10 | 9 |
| `fraq.text2fraq.config` | 5 | 0 |
| `fraq.text2fraq.file_search_parser` | 2 | 4 |
| `fraq.text2fraq.llm_client` | 2 | 4 |
| `fraq.text2fraq.models` | 6 | 2 |
| `fraq.text2fraq.parser_llm` | 4 | 8 |
| `fraq.text2fraq.parser_rules` | 4 | 5 |
| `fraq.text2fraq.router` | 1 | 0 |
| `fraq.text2fraq.session` | 2 | 6 |
| `fraq.text2fraq.shortcuts` | 1 | 8 |
| `fraq.types` | 1 | 0 |
| `main_websocket` | 0 | 2 |
| `project` | 0 | 0 |
