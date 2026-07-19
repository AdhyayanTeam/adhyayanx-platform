"use client";

import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { Textarea } from "@/shared/ui/textarea";
import { Label } from "@/shared/ui/label";
import { submitLost } from "../actions";

interface Props {
  enquiryId: string;
}

export function MarkLostDialog({ enquiryId }: Props) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [reason, setReason] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!reason) return;
    
    setLoading(true);
    setError(null);
    
    const result = await submitLost(enquiryId, { reason });

    setLoading(false);
    if (result.success) {
      setOpen(false);
      setReason("");
    } else {
      setError(result.error || "Something went wrong.");
    }
  };

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger render={
        <Button variant="outline" className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200">
          Mark Lost
        </Button>
      } />
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Mark Enquiry as Lost</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4 pt-4">
          {error && <div className="text-sm text-red-500 font-medium">{error}</div>}
          
          <div className="space-y-2">
            <Label htmlFor="reason">Reason for losing this enquiry</Label>
            <Textarea 
              id="reason" 
              placeholder="e.g. Chose another institute, found fees too high, etc." 
              value={reason} 
              onChange={(e) => setReason(e.target.value)}
              required
              disabled={loading}
              rows={4}
            />
          </div>

          <DialogFooter>
            <Button type="button" variant="outline" onClick={() => setOpen(false)} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" variant="destructive" disabled={loading || !reason}>
              {loading ? "Submitting..." : "Confirm Lost"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
