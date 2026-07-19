"use client";

import { useState, useTransition } from "react";
import { format } from "date-fns";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { useToast } from "@/shared/ui/use-toast";
import { submitBatchAssignment } from "../actions";
import type { CompatibleBatchView } from "../types";
import { Loader2 } from "lucide-react";

interface Props {
  studentId: string;
  enrollmentId: string;
  courseTitle: string;
  currentBatchId: string | null;
  compatibleBatches: CompatibleBatchView[];
  trigger: React.ReactNode;
}

export function AssignBatchDialog({ studentId, enrollmentId, courseTitle, currentBatchId, compatibleBatches, trigger }: Props) {
  const [open, setOpen] = useState(false);
  const [isPending, startTransition] = useTransition();
  const [selectedBatchId, setSelectedBatchId] = useState<string | null>(null);
  const { toast } = useToast();

  const handleAssign = () => {
    if (!selectedBatchId) return;

    startTransition(async () => {
      const result = await submitBatchAssignment(studentId, enrollmentId, selectedBatchId);
      if (result.success) {
        toast({
          title: "Batch Assigned",
          description: "The student has been successfully assigned to the batch.",
        });
        setOpen(false);
        setSelectedBatchId(null);
      } else {
        toast({
          title: "Error",
          description: result.error,
          variant: "destructive",
        });
      }
    });
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={trigger as React.ReactElement} />
      <DialogContent className="sm:max-w-[500px]">
        <DialogHeader>
          <DialogTitle>Assign Batch</DialogTitle>
          <DialogDescription>
            Assign this student to a batch for <strong>{courseTitle}</strong>.
          </DialogDescription>
        </DialogHeader>

        <div className="py-4 space-y-4">
          {compatibleBatches.length === 0 ? (
            <p className="text-sm text-gray-500 italic">No compatible batches found for this course.</p>
          ) : (
            <div className="space-y-3 max-h-[300px] overflow-y-auto pr-2">
              {compatibleBatches.map((batch) => {
                const isCurrent = batch.batch_id === currentBatchId;
                const isSelected = batch.batch_id === selectedBatchId;
                
                return (
                  <div 
                    key={batch.batch_id}
                    onClick={() => !isCurrent && setSelectedBatchId(batch.batch_id)}
                    className={`
                      p-4 rounded-lg border text-left transition-colors cursor-pointer
                      ${isCurrent ? 'bg-gray-50 border-gray-200 cursor-not-allowed opacity-60' : ''}
                      ${!isCurrent && isSelected ? 'border-indigo-600 bg-indigo-50 ring-1 ring-indigo-600' : ''}
                      ${!isCurrent && !isSelected ? 'border-gray-200 hover:border-gray-300 hover:bg-gray-50' : ''}
                    `}
                  >
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium text-gray-900 flex items-center gap-2">
                          {batch.batch_name}
                          {isCurrent && <span className="text-xs bg-gray-200 text-gray-700 px-2 py-0.5 rounded-full">Current</span>}
                        </h4>
                        <p className="text-sm text-gray-500 mt-1">
                          {batch.assigned_student_count} students assigned
                        </p>
                      </div>
                      <div className="text-right">
                        {batch.next_session_starts_at ? (
                          <>
                            <p className="text-xs text-gray-500 font-medium">Next Session</p>
                            <p className="text-sm text-gray-900">{format(new Date(batch.next_session_starts_at), "MMM d, h:mm a")}</p>
                          </>
                        ) : (
                          <p className="text-xs text-gray-500 italic">No upcoming sessions</p>
                        )}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        <DialogFooter>
          <Button variant="outline" onClick={() => setOpen(false)} disabled={isPending}>
            Cancel
          </Button>
          <Button onClick={handleAssign} disabled={!selectedBatchId || isPending}>
            {isPending && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Confirm Assignment
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
