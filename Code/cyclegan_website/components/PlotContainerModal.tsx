import { Button, Modal } from "@nextui-org/react";
import PlotContainer from "./PlotContainer";

interface PlotContainerModalProps {
  visible: boolean;
  closeHandler: () => void;
  files: string[];
  dir: string;
}

const PlotContainerModal = ({
  visible,
  closeHandler,
  files,
  dir,
}: PlotContainerModalProps) => {
  return (
    <Modal
      closeButton
      aria-labelledby="modal-title"
      open={visible}
      onClose={closeHandler}
      width="700px"
    >
      <Modal.Body>
        <PlotContainer id="my_dataviz" files={files} dir={dir} />
      </Modal.Body>
      <Modal.Footer>
        <Button auto flat color="error" onPress={closeHandler}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default PlotContainerModal;
