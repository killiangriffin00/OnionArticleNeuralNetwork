import Button from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';

export default function SatireButtons(props) {
    function onButtonClick(choice) {
        props.setChoices([...props.choices, choice]);
    }

    return (
        <Stack
            gap={2}
            className="col-md-5 mx-auto"
        >
            <Button
                variant="primary"
                size="md"
                onClick={() => onButtonClick(1)}
            >
                Satire
            </Button>
            <Button
                variant="primary"
                size="md"
                onClick={() => onButtonClick(0)}
            >
                Not Satire
            </Button>
        </Stack>
    );
}
