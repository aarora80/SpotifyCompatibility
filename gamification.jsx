import React from "react";
import "./styles.css";

class SpotifySocialGamification extends React.Component {
  handleFriendClick = (friendName) => {
    console.log(`Clicked on ${friendName}'s profile`);
    // You can implement navigation to the friend's profile page here
  };

  handleChallengeClick = (challengeName) => {
    console.log(`Accepted challenge: ${challengeName}`);
    // You can implement displaying challenge details in a modal here
    alert(
      `Challenge Details:\n\n${challengeName}\n\nDescription: Complete a workout playlist with at least 10 tracks.`
    );
  };

  render() {
    return (
      <div className="container">
        <header>
          <h1>Spotify Social & Gamification</h1>
        </header>
        <section className="friends-section">
          <h2>Friends</h2>
          <ul className="friends-list">
            <li onClick={() => this.handleFriendClick("John Doe")}>John Doe</li>
            <li onClick={() => this.handleFriendClick("Jane Smith")}>
              Jane Smith
            </li>
          </ul>
        </section>
        <section className="challenges-section">
          <h2>Challenges</h2>
          <ul className="challenges-list">
            <li
              onClick={() => this.handleChallengeClick("Discover New Artists")}
            >
              Discover New Artists
            </li>
            <li
              onClick={() =>
                this.handleChallengeClick("Create a Workout Playlist")
              }
            >
              Create a Workout Playlist
            </li>
          </ul>
        </section>
      </div>
    );
  }
}

export default SpotifySocialGamification;
