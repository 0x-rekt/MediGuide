const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface TriageRequest {
  symptoms: string;
  latitude: number;
  longitude: number;
  language?: string;
  radius_meters?: number;
  age?: number;
  gender?: string;
}

export interface HospitalResult {
  place_id: string;
  name: string;
  address: string;
  phone: string | null;
  rating: number | null;
  distance_km: number;
  open_now: boolean | null;
  match_score: number;
  match_reason: string;
  google_maps_url: string;
}

export interface TriageResponse {
  report_id: number;
  severity: string;
  severity_score: number;
  severity_color: string;
  urgency_label: string;
  recommended_specialty: string;
  ai_summary: string;
  action_advice: string;
  symptom_card: string;
  confidence_score: number;
  confidence_reason: string;
  red_flags: string[];
  estimated_visit_type: string;
  escalation_action: string;
  escalation_message: string;
  hospitals: HospitalResult[];
  emergency_call_advised: boolean;
  total_hospitals_found: number;
}

export interface BookingRequest {
  hospital_place_id: string;
  hospital_name: string;
  hospital_address: string;
  hospital_phone?: string;
  symptom_report_id?: number;
  patient_name: string;
  patient_age: number;
  patient_gender: string;
  patient_blood_type?: string;
  patient_allergies?: string;
  emergency_contact_name: string;
  emergency_contact_phone: string;
  emergency_contact_email?: string;
  ambulance_requested?: boolean;
  notes?: string;
}

export interface BookingResponse {
  booking_id: number;
  hospital_name: string;
  hospital_address: string;
  hospital_phone: string;
  status: string;
  ambulance_requested: boolean;
  estimated_cost_usd: number | null;
  patient_intake_summary: string;
}

export interface FamilyReportResponse {
  report: string;
}

export async function triageSymptoms(
  data: TriageRequest,
): Promise<TriageResponse> {
  const res = await fetch(`${API_URL}/triage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Triage failed");
  }
  return res.json();
}

export async function createBooking(
  data: BookingRequest,
): Promise<BookingResponse> {
  const res = await fetch(`${API_URL}/bookings`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Booking failed");
  }
  return res.json();
}

export async function generateFamilyReport(
  bookingId: number,
  diagnosisNotes?: string,
  actualCostUsd?: number,
): Promise<FamilyReportResponse> {
  const res = await fetch(`${API_URL}/bookings/family-report`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      booking_id: bookingId,
      diagnosis_notes: diagnosisNotes,
      actual_cost_usd: actualCostUsd,
    }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Report generation failed");
  }
  return res.json();
}
