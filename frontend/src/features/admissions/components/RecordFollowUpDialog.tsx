"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Textarea } from "@/shared/ui/textarea";
import { Label } from "@/shared/ui/label";
import { submitFollowUp } from "../actions";

interface Props {
  enquiryId: string;
}

export function RecordFollowUpDialog({ enquiryId }: Props) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const [date, setDate] = useState("");
  const [notes, setNotes] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!date || !notes) return;
    
    setLoading(true);
    setError(null);
    
    // convert local datetime string to ISO string for backend
    const isoDate = new Date(date).toISOString();

    const result = await submitFollowUp(enquiryId, {
      next_follow_up_at: isoDate,
      notes
    });

    setLoading(false);
    if (result.success) {
      setOpen(false);
      setNotes("");
      setDate("");
    } else {
      setError(result.error || "Something went wrong.");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={<Button variant="outline">Record Follow-up</Button>} />
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Record Follow-up</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 pt-4">
          {error && <div className="text-sm text-red-500 font-medium">{error}</div>}
          
          <div className="space-y-2">
            <Label htmlFor="nextDate">Next Follow-up Date & Time</Label>
            <Input 
              id="nextDate" 
              type="datetime-local" 
              value={date} 
              onChange={(e) => setDate(e.target.value)} 
              required
              disabled={loading}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes">Notes</Label>
            <Textarea 
              id="notes" 
              placeholder="What was discussed?" 
              value={notes} 
              onChange={(e) => setNotes(e.target.value)}
              required
              disabled={loading}
              rows={4}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" disabled={loading || !date || !notes}>
              {loading ? "Saving..." : "Save Follow-up"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
