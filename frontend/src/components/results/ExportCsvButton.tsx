import { Download } from "lucide-react";
import { Button } from "../common/Button";

interface ExportCsvButtonProps {
  onExport: () => void;
}

export function ExportCsvButton({ onExport }: ExportCsvButtonProps) {
  return (
    <Button id="download-button" variant="secondary" onClick={onExport}>
      <Download className="h-3.5 w-3.5" aria-hidden="true" />
      Download predictions
    </Button>
  );
}
