"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { submitAdmission } from "../actions";

interface Props {
  enquiryId: string;
  studentName: string;
  courseName: string;
}

export function ConfirmAdmissionDialog({ enquiryId, studentName, courseName }: Props) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAdmit = async () => {
    setLoading(true);
    setError(null);
    
    const result = await submitAdmission(enquiryId);

    setLoading(false);
    if (result.success) {
      setOpen(false);
      // Wait for server to revalidate and UI to update.
    } else {
      setError(result.error || "Something went wrong.");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button>Admit Student</Button>} />
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Admit {studentName}?</DialogTitle>
        </DialogHeader>
        
        <div className="space-y-4 pt-4">
          {error && <div className="text-sm text-red-500 font-medium">{error}</div>}
          
          <div>
            <h4 className="text-sm font-semibold text-neutral-900">Course</h4>
            <p className="text-sm text-neutral-600">{courseName}</p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900">Student</h4>
            <p className="text-sm text-neutral-600">A new student record will be created<br/>—or—<br/>Existing student record will be used</p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900">Enrollment</h4>
            <p className="text-sm text-neutral-600">Student will be enrolled in {courseName}</p>
          </div>

          <div>
            <h4 className="text-sm font-semibold text-neutral-900">Batch</h4>
            <p className="text-sm text-neutral-600">No batch will be assigned yet</p>
          </div>
        </div>

        <DialogFooter className="mt-6">
          <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={loading}>
            Cancel
          </Button>
          <Button type="button" onClick={handleAdmit} disabled={loading}>
            {loading ? "Submitting..." : "Confirm Admission"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
