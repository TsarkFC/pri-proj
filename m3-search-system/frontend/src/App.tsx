import { useState } from "react";
import {
  getFullTextSearch,
  Query,
  QueryResult,
  buildQuery,
  parseFacets,
} from "./query/Query";
import { SearchResults } from "./SearchResults";
import { SearchFilters } from "./SearchFilters";

function App() {
  const [queryResult, setQueryResult] = useState<QueryResult | null>(null);
  const [queryInput, setQueryInput] = useState("");
  const [queryFacetFields, setQueryFacetFields] = useState<any[]>([]);

  const runQuery = (query: Query, filters?: string[][]) => {
    const q = buildQuery(queryInput, filters);
    console.log(q);
    query(q).then((result) => {
      console.log(result.data);
      setQueryResult(result.data);
      const parsedFacetFields = parseFacets(result.data);
      if (parsedFacetFields.length !== 0)
        setQueryFacetFields(parsedFacetFields);
    });
  };

  return (
    <div id="layout">
      <h1>Portuguese Tech News Explorer</h1>
      <form
        id="search-form"
        onSubmit={(event) => {
          event.preventDefault();
          runQuery(getFullTextSearch);
        }}
      >
        <input
          type="text"
          value={queryInput}
          onChange={(event) => {
            setQueryInput(event.target.value);
          }}
        />
        <button id="search-button" type="submit"><i className="icofont-ui-search"></i></button>
      </form>
      {queryFacetFields.length === 0 ? null : (
        <SearchFilters fields={queryFacetFields} runQuery={runQuery} />
      )}
      {queryResult === null ? null : <SearchResults result={queryResult} />}
    </div>
  );
}

export default App;
