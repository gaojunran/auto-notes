import {NoteResponse, RecordResponse} from "./apis.ts";

// export interface CourseProps {
//     id: number;
//     topic: string;
//     abstract: string;
//     duration: number;
//     tags?: string[];
// }

export interface Cache extends RecordResponse, Partial<NoteResponse> {

}

// export interface Cache extends CourseProps { // 以下均为可选字段
//     raw_recognition?: RawRecognition[];
//     points?: Point[];
//     thoughts?: Question[];
//     exercises?: Question[];
// }


/**
 * ApifoxModel. 注意：当作为NetworkRequest的字段时，仅传name和importance.
 */
export interface Point {
    /**
     * 重要程度，1 - 5。用于后续生成关系图的时候区分点的大小。
     */
    importance: number;
    /**
     * 相关链接
     */
    links?: Link[];
    /**
     * 知识点名称，也是后续建立知识点连接的唯一标识，尽量简洁。
     */
    name: string;
    /**
     * 子主题，用于在康奈尔笔记中一一对应。
     */
    subtitles?: Subtitle[];
    /**
     * 课程总结，Markdown格式。总结课程内容。
     */
    summary?: string;
    [property: string]: any;
}

export interface Link {
    /**
     * 链接地址，URL。大模型经常会生成假的URL，这里建议用大模型生成搜索关键词然后爬虫找链接。
     */
    href: string;
    /**
     * 链接名
     */
    name: string;
    [property: string]: any;
}

/**
 * Subtitle
 */
export interface Subtitle {
    /**
     * 子主题内容，Markdown格式。渲染在康奈尔笔记的右侧。
     */
    md: string;
    /**
     * 子主题的识别内容
     */
    raw_recognition: RawRecognition[];
    /**
     * 子主题名，在康奈尔笔记的左侧。
     */
    subtitle: string;
    [property: string]: any;
}

/**
 * 子主题的识别内容
 *
 * RawRecognition
 */
export interface RawRecognition {
    /**
     * 结束时刻，单位为秒。可选。
     */
    end?: number;
    /**
     * 开始时刻，单位为秒。
     */
    start: number;
    /**
     * 识别内容
     */
    text?: string;
    /**
     * 构建和知识点之间的映射关系
     */
    mapping?: {
        point: Point;
        subtitle: Subtitle;
    }
    [property: string]: any;
}

/**
 * NodeCategory
 */
export interface NodeCategory {
    /**
     * 类别索引, 必须从0开始，和Node中的category节点相对应。
     */
    idx: number;
    /**
     * 类别名, 值和topic相同。
     */
    name: string;
    [property: string]: any;
}

/**
 * NodeLink
 */
export interface NodeLink {
    /**
     * 关系权重, 1-5。数字越大表示关系越紧密。
     */
    weight: number;
    /**
     * 来源节点
     */
    source: string;
    /**
     * 目标节点
     */
    target: string;
    /**
     * 
     */
    isUserGenerated?: boolean;
    [property: string]: any;
}

/**
 * Node
 */
export interface Node {
    /**
     * 节点组别, 对应请求数组的索引，从0开始。
     */
    category: number;
    /**
     * 节点id, 节点的唯一id，关系图连线的时候要使用这个id
     */
    idx?: number;
    /**
     * 节点名称, 可能是topic或者point.name
     */
    name: string;
    /**
     * 节点路由, 用于点击按钮跳转到前端指定的页面。
     */
    route: NoteRoute;
    /**
     * 节点大小, （待定）对于topic来说固定为5，对于point来说为其importance，即1-5.
     */
    size: number;
    [property: string]: any;
}

export interface Lecture {
    id: number;
    topic: string;
    points: Point[];
}

export interface NoteRoute {
    id: number;
    point: string;
}