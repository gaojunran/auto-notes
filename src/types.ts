import {Question} from "./apis.ts";

export interface CourseProps {
    id: number;
    topic: string;
    abstract: string;
    duration: number;
    tags?: string[];
}

export interface Cache extends CourseProps { // 以下均为可选字段
    raw_recognition?: string;
    notes?: string;
    thoughts?: Question[];
    exercises?: Question[];
}