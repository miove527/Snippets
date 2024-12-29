${{
  let lines = mdContent.split("\n");
  function isItemListLine(line) {
    return line.trim().startsWith("-");
  }
  function isHeadingLine(line) {
    return line.trim().startsWith("#");
  }
  let filteredLines = [];

  // 更新正则表达式进行替换
  mdContent = mdContent
    .replace(/\*\*\*/, '---')
    .replaceAll("\\*\\*", "**")
    .replaceAll("Zotero\\_PDF", "Zotero_PDF")
    .replace(/\*\s{3}/gm, '- ')
    .replaceAll("摘要概括:*-", '摘要概括:**');

  lines = mdContent.split("\n");

  for (let i = 0; i < lines.length; i++) {
    let currentLine = lines[i];  // 保留原始行，包括缩进
    let trimmedLine = currentLine.trim(); // 去掉行首尾空格

    // 检查当前行是否包含 <br>
    if (trimmedLine.includes("<br>")) {
      // 如果包含 <br>，则直接添加到 filteredLines 数组中
      filteredLines.push(currentLine);
      continue; // 跳过后续逻辑，因为已经处理了此行
    }

    // 跳过完全的空行  
    if (trimmedLine.length === 0) {
      continue; // 当前行为空，直接跳过
    }

    // 替换行中的所有 * 为 -  
    // currentLine = currentLine.replace(/^\*\s{3}/, '- '); // 处理行首的 `*   `
    // currentLine = currentLine.replace(/\*\s{3}/g, '- '); // 处理其他位置的 `*   `

    let shouldAddCurrentLine = false;
    if (i > 0) {
      // 不是第一行
      let previousLine = lines[i - 1].trim();
      let previousIsItemList = isItemListLine(previousLine);
      let currentIsItemList = isItemListLine(currentLine);

      // 当前行是无序列表项
      if (currentIsItemList) {
        // 如果前一行是无序列表项，则不添加当前行
        if (!previousIsItemList) {
          shouldAddCurrentLine = true;
       }
      } else if (isHeadingLine(previousLine)) {
        // 如果前一行是标题行，添加当前行
        shouldAddCurrentLine = true;
      } else {
        // 如果前一行是其它情况则添加当前行
        shouldAddCurrentLine = true;
      }
    } else {
      // 如果是第一行，直接添加
      shouldAddCurrentLine = true;
    }
     
    // 添加当前行
    if (shouldAddCurrentLine) {
      filteredLines.push(currentLine); // 添加转换后的当前行
      // 检查当前行是否是标题行
      if (isHeadingLine(currentLine)) {
        // 如果是标题行, 检查下一行是否空
        if (i < lines.length - 1) {
          let nextLine = lines[i + 1].trim();
          if (nextLine.length === 0) {
            // 下一行为空，则跳过下一行
            i++;
          }
        }
      }
    }
  }

  return filteredLines.join("\n");    
}}$
