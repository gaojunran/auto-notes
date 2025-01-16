import request from "./request.ts";

export interface RecordResponse {
    rid: number;
    duration: number;
    topic: string;
    abstract: string;
    raw_recognition: string;
}

export interface NoteRequest {
    topic: string;
    raw_recognition: string;
}

export interface NoteResponse {
    notes: string;
}

export interface ThoughtRequest {
    notes: string;
    num: number;
}

export interface Question {
    question: string;
    answer: string;
    analysis?: string;
    knowledge?: string[];
}

export interface ThoughtResponse {
    questions: Question[];
}

export interface ExerciseRequest {
    notes: string;
    num: number;
}

export interface ExerciseResponse {
    exercises: Question[];
}



export const postRecord = async (record: Blob)=> {
    const response: RecordResponse = await request("/record", "POST", record)
    return response;
}

export const getNote = async (note: NoteRequest)=> {
    const response: NoteResponse = await request("/note", "POST", note)
    return response;
}

export const getThought = async (thought: ThoughtRequest)=> {
    const response: ThoughtResponse = await request("/thought", "POST", thought)
    return response;
}

export const getExercise = async (exercise: ExerciseRequest)=> {
    const response: ExerciseResponse = await request("/exercise", "POST", exercise)
    return response;
}

