import { useState } from "react";
import { getFullTextSearch } from "./query/Query";

export interface SearchResultsProps {
  fields: any[];
  runQuery: any;
}

export const SearchFilters = ({ fields, runQuery }: SearchResultsProps) => {
  const [selectedFacetFields] = useState([[""], [""], [""]]);
  const titles = ["Authors", "Entities", "Newspapers"];

  let i = 0;
  return (
    <div id="filters-box">
      <h3 className="subtitle">Filters</h3>
      <div id="filters-flex-container">
      {fields.map((field: any, idx: number) => (
        <div key={idx}>
          <h4 className="filter-title">{titles[i++]}</h4>
          <form>
            {field.map((facet: any[], idx: number) => (
              <div key={idx}>
                <label htmlFor={titles[i - 1] + idx}>
                  {facet[0]} ({facet[1]})
                  <input
                    id={titles[i - 1] + idx}
                    type="checkbox"
                    data-facet={i - 1}
                    onChange={(event) => {
                      const facetPos = event.target.dataset.facet;
                      if (facetPos) {
                        const pos: number = +facetPos;
                        if (event.target.checked)
                          selectedFacetFields[pos].push(facet[0]);
                        else {
                          console.log("UNCHECK")
                          selectedFacetFields[pos] = selectedFacetFields[pos].filter((e) => {
                            console.log(e, facet[0], e !== facet[0])
                            return e !== facet[0]
                          })
                          
                        }
                        console.log(selectedFacetFields)
                        runQuery(getFullTextSearch, selectedFacetFields);
                      }
                    }}
                  />
                </label>
                <br></br>
              </div>
            ))}
          </form>
        </div>
      ))}
      </div>
    </div>
  );
};
