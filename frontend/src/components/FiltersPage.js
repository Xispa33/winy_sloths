import React, { useState, useEffect } from "react";
import axios from "axios";

function FiltersPage() {
  const [traders, setTraders] = useState([]);
  const [minWinRate, setMinWinRate] = useState(0);

  useEffect(() => {
    axios.get(`/traders?min_win_rate=${minWinRate}`).then((response) => {
      setTraders(response.data);
    });
  }, [minWinRate]);

  return (
    <div>
      <h1>Filters Page</h1>
      <input
        type="number"
        value={minWinRate}
        onChange={(e) => setMinWinRate(e.target.value)}
        placeholder="Minimum Win Rate"
      />
      <ul>
        {traders.map((trader) => (
          <li key={trader}>{trader}</li>
        ))}
      </ul>
    </div>
  );
}

export default FiltersPage;
