interface IssueContent {
  type: string,
  content?: IssueContent[],
  text?: string
}

export function extractTextFromIssue(content: IssueContent[]) {
  let plainText = ''
  let previousNodeType: string | null = null

  content.forEach((item) => {
    if (Object.keys(item).some((key) => key === "text")) {
      plainText += item.type === previousNodeType ? item.text : `\n${item.text}`

      previousNodeType = item.type
    }

    if (Object.keys(item).some((key) => key === "content")) {
      plainText += extractTextFromIssue(item.content as IssueContent[])
    }
  })

  return plainText
}
