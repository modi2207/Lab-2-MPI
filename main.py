# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from mpi4py import MPI


def fun(l, chars, n, val):

    generated = l
    if val<len(generated):
        return generated[0:val]
    val=val-len(generated)
    # maximum number of chars we can use is n
    count = len(generated)
    flag = 0
    print("n: , val: ",n,val)
    for i in range(n - 1):
        print("i:",i)
        gen_ = []
        for c1 in generated:
            # if len(c1) < i + 1:
            #     continue
            for c2 in chars:
                new_char = c1 + c2
                print(new_char)
                gen_.append(new_char)
                val = val - 1
                if val == 0:
                    flag = 1
                    break
            if flag == 1:
                break
        generated.extend(gen_)
        if flag == 1:
            break

    return generated


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size= comm.Get_size()

    #print("hello")

    chars = [chr(i) for i in range(97, 123)] + [str(i) for i in range(10)]
    n=0
    if rank == 0:
        x = int(input("Enter X: "))
        n = int(input("Enter N: "))
        value=x//(size-1)
        index = len(chars) // (size - 1)
        rem = x
        return_data = []
        for i in range(size):
            if i==0:
                continue
            else:
                rem = rem - value
                data={}
                if i==size-1:
                    data = {'start': (i-1) * index, 'end': len(chars), 'x': rem+value,'n':n}
                else:
                    data={'start':(i-1)*index,'end':(i-1)*index+index,'x':value,'n':n}
                comm.send(data, dest=i, tag=11)
                print("send data success dest: ",i)

        for i in range(size):
            if i==0:
                continue
            else:
                data=comm.recv(source=i,tag=1)
                #print("recv data length: ",len(data["data"]))
                return_data.extend(data["data"])
        print("length: ",len(return_data))
        print(return_data)
    else:
        data = comm.recv(source=0, tag=11)
        #print("rank {}, and recv data: {}".format(rank,data))
        start=data["start"]
        end=data["end"]
        val=data["x"]
        n=data["n"]
        l=chars[start:end]
        gen=fun(l,chars,n,val)
        #print("rank {}, and gen:  {}".format(rank, len(gen)))
        comm.send({'data':gen},dest=0,tag=1)







# See PyCharm help at https://www.jetbrains.com/help/pycharm/
