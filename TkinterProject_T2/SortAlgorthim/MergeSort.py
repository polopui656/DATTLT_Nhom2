# Thuật toán Merge Sort
def merge(leftData, rightData):
    result = []
    i,j = 0,0
    while i < len(leftData) and j < len(rightData):
        if leftData[i] < rightData[j]:
            result.append(leftData[i])
            draw_bars(leftData, ['green' if x == i else 'blue' for x in range(len(leftData))])
            i += 1
        else:
            result.append(rightData[j])
            draw_bars(rightData, ['green' if x == j else 'blue' for x in range(len(rightData))])
            j += 1
        combined = result + leftData[i:] + rightData[j:]
        draw_bars(combined, ['green' if x == len(result) - 1 else 'blue' for x in range(len(combined))])
        time.sleep(speed_control.get() / 1000)

    result += leftData[i:]
    result += rightData[j:]
    draw_bars(result, ['blue' for _ in range(len(result))])

    return result

def merge_sort(data):
    if len(data) <= 1:
        return data
    midpoint = len(data) // 2
    leftData = merge_sort(data[:midpoint])
    rightData = merge_sort(data[midpoint:])
    return merge(leftData, rightData)
