from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

@dataclass
class KeywordNote:
    keyword: str
    url: str
    note: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None
    is_archived: bool = False

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def summary(self) -> str:
        return f"[{self.keyword}] {self.url} — {self.note[:50]}..." if len(self.note) > 50 else f"[{self.keyword}] {self.url} — {self.note}"

    def tags_text(self) -> str:
        return ", ".join(self.tags) if self.tags else "无标签"


@dataclass
class KeywordNotesCollection:
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def find_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def list_active(self) -> List[KeywordNote]:
        return [n for n in self.notes if not n.is_archived]

    def archive(self, keyword: str) -> int:
        count = 0
        for note in self.notes:
            if note.keyword == keyword and not note.is_archived:
                note.is_archived = True
                count += 1
        return count

    def export_text(self) -> str:
        lines = []
        lines.append("=== 关键词笔记导出 ===")
        lines.append(f"总数: {len(self.notes)}")
        for i, note in enumerate(self.notes, 1):
            status = "归档" if note.is_archived else "活跃"
            lines.append(f"{i}. [{status}] {note.keyword}")
            lines.append(f"   URL: {note.url}")
            lines.append(f"   备注: {note.note}")
            lines.append(f"   标签: {note.tags_text()}")
            lines.append(f"   创建: {note.created_at}")
            lines.append("")
        return "\n".join(lines)


def format_note_table(notes: List[KeywordNote]) -> str:
    header = f"{'序号':<4} {'关键词':<12} {'URL':<40} {'备注':<20} {'标签':<15} {'状态':<6}"
    sep = "-" * len(header)
    rows = [header, sep]
    for i, note in enumerate(notes, 1):
        status = "归档" if note.is_archived else "活跃"
        note_snippet = note.note[:18] + ".." if len(note.note) > 18 else note.note
        tag_snippet = note.tags_text()[:13] + ".." if len(note.tags_text()) > 13 else note.tags_text()
        row = f"{i:<4} {note.keyword:<12} {note.url:<40} {note_snippet:<20} {tag_snippet:<15} {status:<6}"
        rows.append(row)
    return "\n".join(rows)


def demo_usage() -> KeywordNotesCollection:
    collection = KeywordNotesCollection()

    note1 = KeywordNote(
        keyword="开云",
        url="https://www.cloud-bet-kaiyun.com.cn",
        note="开云官方入口，提供体育赛事投注服务",
        tags=["体育", "博彩", "入口"],
    )

    note2 = KeywordNote(
        keyword="开云体育",
        url="https://www.cloud-bet-kaiyun.com.cn/sports",
        note="开云体育板块，包含足球、篮球等赛事",
        tags=["体育", "足球", "篮球"],
    )

    note3 = KeywordNote(
        keyword="优惠活动",
        url="https://www.cloud-bet-kaiyun.com.cn/promotions",
        note="当前优惠：首存赠送100%",
        tags=["优惠", "活动"],
    )

    note4 = KeywordNote(
        keyword="开云",
        url="https://www.cloud-bet-kaiyun.com.cn/download",
        note="移动端下载，支持Android和iOS",
        tags=["下载", "APP"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)
    collection.add(note4)
    return collection


if __name__ == "__main__":
    collection = demo_usage()
    print(collection.export_text())
    print("\n--- 表格输出 ---")
    active_notes = collection.list_active()
    print(format_note_table(active_notes))
    print("\n--- 按关键词查找：开云 ---")
    for note in collection.find_by_keyword("开云"):
        print(note.summary())