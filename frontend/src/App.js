import { useEffect, useState } from 'react';
import SatireButtons from './Buttons';
import output from './output.csv';

const NUM_ENTRIES_FOR_USER = 20;

export default function App() {
    const [data, setData] = useState([]);
    const [text, setText] = useState(null);
    const [current, setCurrent] = useState({ text: 'Loading...', guess: -1 });
    const [userChoices, setUserChoices] = useState([]);
    const [userScore, setUserScore] = useState(0);
    const [AIScore, setAIScore] = useState(0);

    useEffect(() => {
        fetch(output)
            .then((out) => out.text())
            .then((text) => {
                const rows = text.split('\n');
                const d = rows.map((row) => {
                    const columns = row.split(',');
                    return {
                        text: columns[0],
                        AIguess: parseInt(columns[1][0]),
                        actual: parseInt(columns[2][0]),
                    };
                });

                const randomEntries = pickRandomEntries(
                    NUM_ENTRIES_FOR_USER,
                    d.length
                );
                const randomData = randomEntries.map((index) => d[index]);
                setData(randomData);
                setCurrent(randomData[0]);
            });
    }, []);

    const pickRandomEntries = (count, data_length) => {
        const randomEntries = [];
        while (randomEntries.length < Math.min(count, data_length)) {
            const randomIndex = Math.floor(Math.random() * data_length);
            if (!randomEntries.includes(randomIndex)) {
                randomEntries.push(randomIndex);
            }
        }
        return randomEntries;
    };

    useEffect(() => {
        const index = userChoices.length + 1;
        if (index < data.length) {
            setCurrent(data[index]);
            return;
        } else if (index === data.length) {
            getUserScore();
            getAIScore();
            setCurrent({ text: 'Done!', guess: -1 });
        }
    }, [userChoices]);

    const getUserScore = () => {
        let score = 0;
        for (let i = 0; i < data.length; i++) {
            if (userChoices[i] === data[i].actual) {
                score++;
            }
        }
        setUserScore(score);
    };

    const getAIScore = () => {
        let score = 0;
        for (let i = 0; i < data.length; i++) {
            if (data[i].actual === data[i].AIguess) {
                score++;
            }
        }
        setAIScore(score);
    };

    return (
        <div>
            {current.text}
            <SatireButtons
                setChoices={setUserChoices}
                choices={userChoices}
            />
            {userChoices.length < data.length - 1
                ? ''
                : 'Your Score: ' + userScore + ', AI Score: ' + AIScore}
        </div>
    );
}
