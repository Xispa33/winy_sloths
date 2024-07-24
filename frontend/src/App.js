import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import FiltersPage from "./components/FiltersPage";
import Leaderboard from "./components/Leaderboard";
import Staking from "./components/Staking";

function App() {
  return (
    <Router>
      <Switch>
        VVS
        <Route path="/filters" component={FiltersPage} />
        <Route path="/leaderboard" component={Leaderboard} />
        <Route path="/staking" component={Staking} />
      </Switch>
    </Router>
  );
}

export default App;
