import Button from 'react-bootstrap/Button';

export default function SatireButtons(props) {
    function onButtonClick(choice) {
        props.setChoices([...props.choices, choice]);
    }

    return (
        <div>
            <Button onClick={() => onButtonClick(0)}>Not Satire</Button>
            <Button onClick={() => onButtonClick(1)}>Satire</Button>
        </div>
    );
}
