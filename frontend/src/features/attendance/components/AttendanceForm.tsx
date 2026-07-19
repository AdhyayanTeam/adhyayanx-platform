"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { ToggleGroup, ToggleGroupItem } from "@/shared/ui/toggle-group";
import { Button } from "@/shared/ui/button";
import type { SessionAttendanceSheetView } from "../types";
import { submitAttendanceAction } from "../actions";

export function AttendanceForm({ 
  sessionId, 
  initialRoster 
}: { 
  sessionId: string; 
  initialRoster: SessionAttendanceSheetView[] 
}) {
  const router = useRouter();
  const [isPending, startTransition] = useTransition();
  const [error, setError] = useState<string | null>(null);

  // Local state for attendance records
  const [records, setRecords] = useState<Record<string, "PRESENT" | "ABSENT" | null>>(() => {
    const initial: Record<string, "PRESENT" | "ABSENT" | null> = {};
    initialRoster.forEach(student => {
      initial[student.student_id] = null;
    });
    return initial;
  });

  const presentCount = Object.values(records).filter(s => s === "PRESENT").length;
  const absentCount = Object.values(records).filter(s => s === "ABSENT").length;
  const unmarkedCount = Object.values(records).filter(s => s === null).length;
  
  const canSubmit = unmarkedCount === 0;

  const handleMarkAllPresent = () => {
    setRecords(prev => {
      const next = { ...prev };
      Object.keys(next).forEach(key => {
        next[key] = "PRESENT";
      });
      return next;
    });
  };

  const handleSubmit = async () => {
    if (!canSubmit) return;
    
    startTransition(async () => {
      setError(null);
      const payloadRecords = Object.entries(records).map(([student_id, status]) => ({
        student_id,
        status: status as "PRESENT" | "ABSENT"
      }));

      const res = await submitAttendanceAction(sessionId, { records: payloadRecords });
      
      if (res?.error) {
        setError(res.error);
      } else {
        router.refresh(); // Tells Next.js to refetch the server component
      }
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-white p-4 rounded-lg border border-neutral-200 shadow-sm">
        <div className="flex items-center gap-6">
          <div className="text-sm">
            <span className="font-semibold text-neutral-900">{initialRoster.length}</span> <span className="text-neutral-500">Total</span>
          </div>
          <div className="text-sm">
            <span className="font-semibold text-green-600">{presentCount}</span> <span className="text-neutral-500">Present</span>
          </div>
          <div className="text-sm">
            <span className="font-semibold text-red-600">{absentCount}</span> <span className="text-neutral-500">Absent</span>
          </div>
          {unmarkedCount > 0 && (
            <div className="text-sm">
              <span className="font-semibold text-yellow-600">{unmarkedCount}</span> <span className="text-neutral-500">Unmarked</span>
            </div>
          )}
        </div>
        
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={handleMarkAllPresent}>
            Mark All Present
          </Button>
          <Button 
            onClick={handleSubmit} 
            disabled={!canSubmit || isPending}
            className={isPending ? "opacity-50" : ""}
          >
            {isPending ? "Submitting..." : "Submit Attendance"}
          </Button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md text-sm">
          {error}
        </div>
      )}

      <div className="bg-white rounded-lg border border-neutral-200 shadow-sm overflow-hidden">
        <div className="divide-y divide-neutral-100">
          {initialRoster.map((student) => (
            <div key={student.student_id} className="p-4 flex items-center justify-between hover:bg-neutral-50 transition-colors">
              <div>
                <div className="font-medium text-neutral-900">{student.name}</div>
                <div className="text-sm text-neutral-500">{student.email}</div>
              </div>
              
              <ToggleGroup 
                type="single" 
                // @ts-expect-error Base UI toggle group type mismatch for single value
                value={records[student.student_id] || ""}
                onValueChange={(val: any) => {
                  const singleVal = Array.isArray(val) ? val[0] : val;
                  if (singleVal === "PRESENT" || singleVal === "ABSENT") {
                    setRecords(prev => ({ ...prev, [student.student_id]: singleVal }));
                  }
                }}
                className="bg-neutral-100 p-1 rounded-md"
              >
                <ToggleGroupItem 
                  value="PRESENT" 
                  aria-label="Present"
                  className="data-[state=on]:bg-green-100 data-[state=on]:text-green-800 text-neutral-600 px-4 h-8"
                >
                  Present
                </ToggleGroupItem>
                <ToggleGroupItem 
                  value="ABSENT" 
                  aria-label="Absent"
                  className="data-[state=on]:bg-red-100 data-[state=on]:text-red-800 text-neutral-600 px-4 h-8"
                >
                  Absent
                </ToggleGroupItem>
              </ToggleGroup>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
